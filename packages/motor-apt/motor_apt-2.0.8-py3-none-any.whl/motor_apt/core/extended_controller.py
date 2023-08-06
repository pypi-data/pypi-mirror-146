# -*- coding: utf-8 -*-
"""
Created on 17.07.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""

try:
    import queue
except ImportError:
    import Queue as queue
from abc import ABCMeta
import os
import struct as st
import threading
from threading import Thread
import time
import pickle
import logging

from motor_apt.core.pyAPT import message
from motor_apt.core.pyAPT.message import Message
from motor_apt.core.pyAPT.controller import Controller, ControllerStatus
from motor_apt.core.message_listener import MessageListener
from motor_apt.core.timeout_exception import TimeoutException


class ExtendedController(Controller):
    """
    A exteneded controller for Thorlabs stages
    """
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self._send_message_lock = threading.Lock()
        self.force_permanent_message_production = kwargs.get('force_permanent_message_production', False)
        if 'force_permanent_message_production' in kwargs:
            del kwargs['force_permanent_message_production']
        self._persist_enccount = kwargs.get('persist_enccount', False)
        if 'persist_enccount' in kwargs:
            del kwargs['persist_enccount']
        super(ExtendedController, self).__init__(*args, **kwargs)

        self._keep_alive_thread = None
        self._stop_requested = False

        if self._persist_enccount:
            self._load_last_enc_position()

        if self.force_permanent_message_production:
            self.resume_end_of_move_messages()
        else:
            self.suspend_end_of_move_messages()

        self.message_listener = MessageListener(self)
        self.message_listener.start()
        self._start_alive_worker()

    def __exit__(self, type_, value, traceback):
        """
        Method override called when exiting with statement.
        """
        self.close()

    def __del__(self):
        """
        Destructor override
        """
        if hasattr(self, '_device'): # only if the init was reasonably complete
            self.close()

    def close(self):
        """
        Function taking care of stopping the controller and closing the connection to it while saving
        current encoder count.
        """
        self.stop_update_messages()
        self.stop(wait=True)
        if self._persist_enccount:
            self._save_last_enc_position()
        self.message_listener.closing = True
        super(ExtendedController, self).close()
        self.message_listener.stop()

    def _load_last_enc_position(self):
        """
        As CR1 stage does ot have homing capabilities it is crucial to always keep the current encoder count, so that
        it is not necessary to recalibrate after each power-on.

        This function loads last encoder count from a file.
        """
        if os.path.isfile("enccnt"):
            enccnt = pickle.load(open("enccnt", "rb"))
            self.set_encoder_counter(enc_count=enccnt)

    def _save_last_enc_position(self):
        """
        As CR1 stage does ot have homing capabilities it is crucial to always keep the current encoder count, so that
        it is not necessary to recalibrate after each power-on.

        This function saves last encoder count into a file.
        """
        enccnt = self.encoder_counter()
        pickle.dump(enccnt, open("enccnt", "wb"))

    def suspend_end_of_move_messages(self):
        if self.force_permanent_message_production is True:
            return
        else:
            super(ExtendedController, self).suspend_end_of_move_messages()

    def jog(self, channel=1, direction=2, wait=True):
        """
        channel always 1 for TDC001
        direction 1 or 2
            - real direction stage-dependent
            - for CR1/M-Z7: CCW=1 CW=2

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor

        WARNING: wait=True and jog_mode=1 (continuous) results in infinite loop!
        """

        if direction not in [1, 2]:
            raise ValueError("Allowed values for direction are only 1 (forward) and 2 (backward)!")

        if wait:
            self.resume_end_of_move_messages()
        else:
            self.suspend_end_of_move_messages()

        movemsg = Message(message.MGMSG_MOT_MOVE_JOG, param1=channel, param2=direction)
        self._send_message(movemsg)

        if wait:
            self.message_listener.set_no_wait_message_flag(value=False)
            msg = self._wait_message(message.MGMSG_MOT_MOVE_COMPLETED)
            sts = ControllerStatus(self, msg.datastring)
            # I find sometimes that after the move completed message there is still
            # some jittering. This aims to wait out the jittering so we are
            # stationary when we return
            while sts.velocity_apt:
                time.sleep(0.01)
                sts = self.status()
            return sts
        else:
            self.message_listener.set_no_wait_message_flag()
            return None

    def set_jog_parameters(self, channel=1, jog_mode=2, step_size=1, acceleration=None, max_velocity=None, stop_mode=2):
        """
        Sets the velocity jog parameters of the controller. Note that
        minimum velocity cannot be set, because protocol demands it is always
        zero.

        When called without arguments, max acceleration and max velocity will
        be set to self.max_acceleration and self.max_velocity
        """
        if jog_mode not in [1, 2]:
            raise ValueError("Allowed values for jog mode are only 1 (continuous) and 2 (step)!")

        if step_size < 0:
            raise ValueError("Step size can't be negative")

        if acceleration is None:
            acceleration = self.max_acceleration
        elif acceleration < 0:
            raise ValueError("Acceleration can't be negative!")
        elif acceleration > self.max_acceleration:
            raise ValueError("Acceleration over maximum acceleration limit!")

        if max_velocity is None:
            max_velocity = self.max_velocity
        elif max_velocity < 0:
            raise ValueError("Maximum velocity can't be negative!")
        elif max_velocity > self.max_velocity:
            raise ValueError("Maximum velocity over maximum velocity limit!")

        if stop_mode not in [1, 2]:
            raise ValueError("Allowed values for stop mode are only 1 (immediate) and 2 (profiled)!")

        step_size_apt = int(round(step_size * self.position_scale))
        acc_apt = int(round(acceleration * self.acceleration_scale))
        max_vel_apt = int(round(max_velocity * self.velocity_scale))

        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for jog mode, continuous = 1, step mode = 2
        i: 4 bytes for step size
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        H: 2 bytes for stop mode, immediate = 1, profiled = 2
        """
        params = st.pack('<HHiiiiH', channel, jog_mode, step_size_apt, 0, acc_apt, max_vel_apt, stop_mode)
        setmsg = Message(message.MGMSG_MOT_SET_JOGPARAMS, data=params)
        self._send_message(setmsg)

    def jog_parameters(self, channel=1, raw=False):
        """
        Returns the velocity jog parameters of the controller. That is jog mode,
        step size, minimum start velocity, acceleration, maximum velocity and
        stop mode.

        channel specifies the channel to query.

        raw specifies whether the raw controller values are returned, or the scaled
        real world values. Defaults to False.

        Example:
          jog_mode, step_size, min_vel, acc, max_vel, stop_mode = con.jog_parameters()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_JOGPARAMS, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_JOGPARAMS)

        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for jog mode, continuous = 1, step mode = 2
        i: 4 bytes for step size
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        H: 2 bytes for stop mode, immediate = 1, profiled = 2
        """
        ch, jog_mode, step_size, min_vel, acc, max_vel, stop_mode = st.unpack('<HHiiiiH', getmsg.datastring)

        if not raw:
            step_size /= self.position_scale
            min_vel /= self.velocity_scale
            max_vel /= self.velocity_scale
            acc /= self.acceleration_scale

        return jog_mode, step_size, min_vel, acc, max_vel, stop_mode

    def set_limit_switch_parameters(self, cw_hard=1, ccw_hard=1, cw_soft=0, ccw_soft=0, soft_mode=1, channel=1):
        """
        Sets the limit switch parameters of the controller.

        For hard limit:
        The operation of the hardware limit switch when contact is made
        0x01 - Ignore switch or switch not present.
        0x02 - Switch makes on contact.
        0x03 - Switch breaks on contact.
        0x04 - Switch makes on contact - only used for homes (e.g.limit switched rotation stages).
        0x05 - Switch breaks on contact - only used for homes (e.g.limit switched rotations stages).
        0x06 - For PMD based brushless servo controllers only - uses index mark for homing.
        Note. Set upper bit to swap CW and CCW limit switches in code. Both CWHardLimit and CCWHardLimit structure members
        will have the upper bit set when limit switches have been physically swapped. 0x80 // bitwise OR'd with one of the settings above.

        For soft limit:
        Software limit in position steps. A 32 bit unsigned long value, the scaling factor between real time values and
        this parameter is 1 mm is equivalent to 134218. For example, to set the software limit switch to 100mm, send a value of 13421800.
        (Not applicable to TDC001 units)

        Software limit switch mode:
        0x01 - Ignore Limit
        0x02 - Stop Immediate at Limit
        0x03 - Profiled Stop at limit
        0x80 - Rotation Stage Limit (bitwise OR'd with one of the settings above)
        (Not applicable to TDC001 units)
        """
        hw_limit_params = {0x01, 0x02, 0x03, 0x04, 0x05}

        if cw_hard not in hw_limit_params:
            raise ValueError("HW limit switch setting accepts values (128 + ) 1 - 6. See docstring for their meanings.")
        if ccw_hard not in hw_limit_params:
            raise ValueError("HW limit switch setting accepts values (128 + ) 1 - 6. See docstring for their meanings.")

        if cw_soft < 0:
            raise ValueError("SW limit switch position can't be negative.")
        if ccw_soft < 0:
            raise ValueError("SW limit switch position can't be negative.")

        if soft_mode not in [0x01, 0x02, 0x03, 0x81, 0x82, 0x83]:
            raise ValueError("SW limit switch mode setting accepts values (128 + ) 1 - 3. See docstring for their meanings.")

        cw_soft_apt = int(round(cw_soft * self.position_scale))
        ccw_soft_apt = int(round(ccw_soft * self.position_scale))

        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for CW hard limit
        H: 2 bytes for CCW hard limit
        i: 4 bytes for CW soft limit (not applicable to TDC001)
        i: 4 bytes for CCW soft limit (not applicable to TDC001)
        H: 2 bytes for soft limit mode (not applicable to TDC001)
        """
        params = st.pack('<HHHiiH', channel, cw_hard, ccw_hard, cw_soft_apt, ccw_soft_apt, soft_mode)
        setmsg = Message(message.MGMSG_MOT_SET_LIMSWITCHPARAMS, data=params)
        self._send_message(setmsg)

    def limit_switch_parameters(self, channel=1, raw=False):
        """
        Returns the limit switch parameters, That is clockwise hard limit,
        counter-clockwise hard limit, clockwise soft limit, counter-clockwise
        soft limit and soft limit mode.

        channel specifies the channel to query.

        raw specifies whether the raw controller values are returned, or the scaled
        real world values. Defaults to False.

        Example:
          cw_hard, ccw_hard, cw_soft, ccw_soft, soft_mode = con.limit_switch_parameters()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_LIMSWITCHPARAMS, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_LIMSWITCHPARAMS)

        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for CW hard limit
        H: 2 bytes for CCW hard limit
        i: 4 bytes for CW soft limit (not applicable to TDC001)
        i: 4 bytes for CCW soft limit (not applicable to TDC001)
        H: 2 bytes for soft limit mode (not applicable to TDC001)
        """
        ch, cw_hard, ccw_hard, cw_soft, ccw_soft, soft_mode = st.unpack('<HHHiiH', getmsg.datastring)

        if not raw:
            cw_soft /= self.position_scale  # not sure it is correct, TDC001 does not support soft switches anyway
            ccw_soft /= self.position_scale  # not sure it is correct, TDC001 does not support soft switches anyway
        return cw_hard, ccw_hard, cw_soft, ccw_soft, soft_mode

    def set_backlash_settings(self, backlash_distance, channel=1):
        """
        Sets the backlash settings. Currently, only backlash distance can be set.
        """

        # if backlash_distance < 0:
        #     raise ValueError("Backlash distance can't be negative!")

        backlash_distance_apt = int(round(backlash_distance * self.position_scale))

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for backlash distance
        """
        params = st.pack('<Hi', channel, backlash_distance_apt)
        setmsg = Message(message.MGMSG_MOT_SET_GENMOVEPARAMS, data=params)
        self._send_message(setmsg)

    def backlash_settings(self, channel=1, raw=False):
        """
        Returns the backlash settings. As of 04.05.2015 it is only backlash distance.

        channel specifies the channel to query.

        raw specifies whether the raw controller values are returned, or the scaled
        real world values. Defaults to False.

        Example:
          backlash_distance = con.backlash_settings()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_GENMOVEPARAMS, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_GENMOVEPARAMS)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for backlash distance
        """
        ch, backlash_distance = st.unpack('<Hi', getmsg.datastring)

        if not raw:
            backlash_distance /= self.position_scale

        return backlash_distance

    def set_dc_pid_parameters(self, proportional_gain, integral_gain, differential_gain, integral_limit=0, filter_control=0x0F, channel=1):
        """
        Sets pid parameters of the DC controller. Available parameters are proportional gain, integral gain, differential gain,
        integral limit and filter control.

        First four accept values from the interval <0; 32767>.
        If integral limit is set to 0 it is ignored.
        Filter control controls which of first four are used by setting the corresponding bit to 1.
        E.g. if all four are used filter control is (1,1,1,1) => 0x0F
        """

        if proportional_gain % 1 != 0 or proportional_gain < 0 or proportional_gain > 32767:
            raise ValueError("Proportional gain value must be whole number from interval <0; 32767>")
        if integral_gain % 1 != 0 or integral_gain < 0 or integral_gain > 32767:
            raise ValueError("Integral gain value must be whole number from interval <0; 32767>")
        if differential_gain % 1 != 0 or differential_gain < 0 or differential_gain > 32767:
            raise ValueError("Differential gain value must be whole number from interval <0; 32767>")
        if integral_limit % 1 != 0 or integral_limit < 0 or integral_limit > 32767:
            raise ValueError("Integral limit value must be whole number from interval <0; 32767>")
        if filter_control % 1 != 0 or filter_control < 0 or filter_control > 0x0F:
            raise ValueError("Filter control must be from interval <0x00; 0x0F>")

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for proportional gain; <0; 32767>
        i: 4 bytes for integral gain; <0; 32767>
        i: 4 bytes for differential gain; <0; 32767>
        i: 4 bytes for integral limit; <0; 32767>;
            used to cap the value of the lntegrator to prevent runaway of the integral sum at the output;
            if set to 0 then the integration term in the PID loop is ignored
        H: 2 bytes for filter control; identifies which of the above parameters are applied by setting the corresponding bit to 1
        """
        params = st.pack('<HiiiiH', channel, proportional_gain, integral_gain, differential_gain, integral_limit, filter_control)
        setmsg = Message(message.MGMSG_MOT_SET_DCPIDPARAMS, data=params)
        self._send_message(setmsg)

    def dc_pid_parameters(self, channel=1):
        """
        Returns pid parameters of DC controller.

        channel specifies the channel to query.

        Example:
          proportional_gain, integral_gain, differential_gain, integral_limit, filter_control = con.dc_pid_parameters()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_DCPIDPARAMS, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_DCPIDPARAMS)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for proportional gain; <0; 32767>
        i: 4 bytes for integral gain; <0; 32767>
        i: 4 bytes for differential gain; <0; 32767>
        i: 4 bytes for integral limit; <0; 32767>;
            used to cap the value of the lntegrator to prevent runaway of the integral sum at the output;
            if set to 0 then the integration term in the PID loop is ignored
        H: 2 bytes for filter control; identifies which of the above parameters are applied by setting the corresponding bit to 1
        """
        ch, proportional_gain, integral_gain, differential_gain, integral_limit, filter_control = st.unpack('<HiiiiH', getmsg.datastring)

        return proportional_gain, integral_gain, differential_gain, integral_limit, filter_control

    def move_relative(self, rel_pos_mm, channel=1, wait=True):
        """
        Tells the stage to move relative to current position by N mm.

        When wait is True, this method only returns when the stage has signaled
        that it has finished moving.

        Note that the wait is implemented by waiting for MGMSG_MOT_MOVE_COMPLETED,
        then querying status until the position returned matches the requested
        position, and velocity is zero.

        This method returns an instance of ControllerStatus if wait is True, None
        otherwise.

        If the requested position is beyond the limits defined in
        self.linear_range, and OutOfRangeError will be thrown.
        """

        # if self.soft_limits and not self._position_in_range(abs_pos_mm):
        #   raise OutOfRangeError(abs_pos_mm, self.linear_range)

        rel_pos_apt = int(round(rel_pos_mm * self.position_scale))

        """
        <: little endian
        H: 2 bytes for channel id
        i: 4 bytes for relative position
        """
        params = st.pack('<Hi', channel, rel_pos_apt)

        if wait:
            self.resume_end_of_move_messages()
        else:
            self.suspend_end_of_move_messages()
        movemsg = Message(message.MGMSG_MOT_MOVE_RELATIVE, data=params)
        self._send_message(movemsg)

        if wait:
            self.message_listener.set_no_wait_message_flag(value=False)
            msg = self._wait_message(message.MGMSG_MOT_MOVE_COMPLETED)
            sts = ControllerStatus(self, msg.datastring)
            # I find sometimes that after the move completed message there is still
            # some jittering. This aims to wait out the jittering so we are
            # stationary when we return
            while sts.velocity_apt:
                time.sleep(0.01)
                sts = self.status()
            return sts
        else:
            self.message_listener.set_no_wait_message_flag()
            return None

    def move_absolute(self, abs_pos_mm, channel=1, wait=True):
        """
        Tells the stage to goto the specified absolute position, in mm.

        abs_pos_mm will be clamped to self.linear_range

        When wait is True, this method only returns when the stage has signaled
        that it has finished moving.

        Note that the wait is implemented by waiting for MGMSG_MOT_MOVE_COMPLETED,
        then querying status until the position returned matches the requested
        position, and velocity is zero

        This method returns an instance of ControllerStatus if wait is True, None
        otherwise.

        If the requested position is beyond the limits defined in
        self.linear_range, and OutOfRangeError will be thrown.
        """

        # if self.soft_limits and not self._position_in_range(abs_pos_mm):
        #   raise OutOfRangeError(abs_pos_mm, self.linear_range)

        abs_pos_apt = int(round(abs_pos_mm * self.position_scale))

        """
        <: little endian
        H: 2 bytes for channel id
        i: 4 bytes for absolute position
        """
        params = st.pack('<Hi', channel, abs_pos_apt)

        if wait:
            self.resume_end_of_move_messages()
        else:
            self.suspend_end_of_move_messages()

        movemsg = Message(message.MGMSG_MOT_MOVE_ABSOLUTE, data=params)
        self._send_message(movemsg)

        if wait:
            self.message_listener.set_no_wait_message_flag(value=False)
            msg = self._wait_message(message.MGMSG_MOT_MOVE_COMPLETED)
            sts = ControllerStatus(self, msg.datastring)
            # I find sometimes that after the move completed message there is still
            # some jittering. This aims to wait out the jittering so we are
            # stationary when we return
            while sts.velocity_apt:
                time.sleep(0.01)
                sts = self.status()
            return sts
        else:
            self.message_listener.set_no_wait_message_flag()
            return None

    def move_continuous(self, direction, channel=1):
        """
        Tells the stage to move continuously in selected direction.

        direction = 1 => forward movement
        direction = 2 => backward movement

        Moves until either a stop command is called, or a limit switch is reached.

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor
        """
        if direction not in [1, 2]:
            raise ValueError("Allowed values for direction are only 1 (forward) and 2 (backward)!")

        self.message_listener.set_no_wait_message_flag(value=False)

        movemsg = Message(message.MGMSG_MOT_MOVE_VELOCITY, param1=channel, param2=direction)
        self._send_message(movemsg)

        return None

    def set_home_parameters(self, channel=1, direction=2, limit_switch=1, velocity=None, distance_offset=0):
      """
      Sets homing parameters of the controller.

      direction = 1 => forward movement
      direction = 2 => backward movement

      limit_switch - CR1 accepts only 1 and 4

      When called without arguments, velocity will be set to self.max_velocity
      """

      if direction not in [1, 2]:
          raise ValueError("Allowed values for direction are only 1 (forward) and 2 (backward)!")

      if limit_switch not in [1, 4]:  # should be verified with Thorlabs
          raise ValueError("Allowed values for limit switch (for CR1 and Z812B) are only 1 (unknown) and 4 (unknown)!")

      if velocity == None:
        velocity = self.max_velocity
      elif velocity < 0:
        raise ValueError("Velocity can't be negative!")
      elif velocity > self.max_velocity:
        raise ValueError("Velocity over maximum velocity limit!")

      if distance_offset < 0:
          raise ValueError("Distance offset can't be negative!")

      vel_apt = int(velocity * self.velocity_scale + 0.5)
      dist_offset_apt = int(distance_offset * self.position_scale + 0.5)

      """
      <: little endian
      H: 2 bytes for channel id
      H: 2 bytes for home direction; 1 = forward; 2 = reverse
      H: 2 bytes for limit switch; 1 || 4 for CR1
      i: 4 bytes for homing velocity
      i: 4 bytes for offset distance
      """
      params = st.pack('<HHHii', channel, direction, limit_switch, vel_apt, dist_offset_apt)
      setmsg = Message(message.MGMSG_MOT_SET_HOMEPARAMS, data=params)
      self._send_message(setmsg)

    def home_parameters(self, channel=1, raw=False):
      """
      Returns the homing parameters. That is homing direction, limit switch, homing velocity and offset distance.

      channel specifies the channel to query.

      raw specifies whether the raw controller values are returned, or the scaled
      real world values. Defaults to False.

      Example:
        direction, limit_switch, velocity, offset = con.home_parameters()
      """
      reqmsg = Message(message.MGMSG_MOT_REQ_HOMEPARAMS, param1=channel)
      self._send_message(reqmsg)

      getmsg = self._wait_message(message.MGMSG_MOT_GET_HOMEPARAMS)

      """
      <: little endian
      H: 2 bytes for channel id
      H: 2 bytes for home direction; 1 || 2
      H: 2 bytes for limit switch
      i: 4 bytes for homing velocity
      i: 4 bytes for offset distance
      """
      ch, direction, limit_switch, velocity, offset = st.unpack('<HHHii',getmsg.datastring)

      if not raw:
        velocity /= self.velocity_scale
        offset /= self.position_scale

      return direction, limit_switch, velocity, offset

    def home(self, channel=1, wait=False):
      """
      Moves the stage to home position.

      channel always 1 for TDC001

      packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor
      """

      if wait:
        self.resume_end_of_move_messages()
      else:
        self.suspend_end_of_move_messages()

      homemsg = Message(message.MGMSG_MOT_MOVE_HOME, param1=channel)
      self._send_message(homemsg)

      if wait:
        msg = self._wait_message(message.MGMSG_MOT_MOVE_HOMED)
        sts = self.status()
        while sts.velocity_apt:
          time.sleep(0.01)
          sts = self.status()
        return sts
      else:
        self.message_listener.set_no_wait_message_flag()
        return None

    def stop(self, channel=1, immediate=True, wait=True):
        """
        Stops the motor on the specified channel. If immediate is True, then the
        motor stops immediately, otherwise it stops in a profiled manner, i.e.
        decelerates according to max acceleration from current velocity down to zero

        If wait is True, then this method returns only when MGMSG_MOT_MOVE_STOPPED
        is read, and controller reports velocity of 0.

        This method returns an instance of ControllerStatus if wait is True, None
        otherwise.
        """
        sts = self.status()
        if not sts.moving:
            return None

        if wait:
            self.resume_end_of_move_messages()
        else:
            self.suspend_end_of_move_messages()

        stopmsg = Message(message.MGMSG_MOT_MOVE_STOP,
                          param1=channel,
                          param2=1 if immediate else 2)
        self._send_message(stopmsg)

        if wait:
            try:
                self._wait_message(message.MGMSG_MOT_MOVE_STOPPED, timeout_ms=1500)
                sts = self.status()
                while sts.velocity_apt:
                    time.sleep(0.001)
                    sts = self.status()
                return sts
            except TimeoutException:
                logging.debug("No MGMSG_MOT_MOVE_STOPPED received")
                endtime = time.time() + 500 / float(1000)
                sts = self.status()
                while sts.velocity_apt:
                    remaining = endtime - time.time()
                    if remaining <= 0.0:
                        raise Exception("Stop command failed")
                    time.sleep(0.001)
                    sts = self.status()
                return sts
        else:
            return None

    def disconnect(self):
        """
        Sent by the hardware unit or host when either wants to disconnect from the Ethernet/USB bus.
        """
        reqmsg = Message(message.MGMSG_HW_DISCONNECT)
        self._send_message(reqmsg)

    def set_position_counter(self, position, channel=1):
        """
        Sets the 'live' position count in the controller.
        """

        pos_apt = int(round(position * self.position_scale))

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for position
        """
        params = st.pack('<Hi', channel, pos_apt)
        setmsg = Message(message.MGMSG_MOT_SET_POSCOUNTER, data=params)
        self._send_message(setmsg)

    def position_counter(self, channel=1, raw=False):
        """
        Returns the 'live' position count in the controller.

        channel specifies the channel to query.

        raw specifies whether the raw controller values are returned, or the scaled
        real world values. Defaults to False.

        Example:
          position = con.position_counter()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_POSCOUNTER, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_POSCOUNTER)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for position
        """
        ch, position = st.unpack('<Hi', getmsg.datastring)

        if not raw:
            position /= self.position_scale

        return position

    def set_encoder_counter(self, enc_count, channel=1):
        """
        Sets the encoder count in the controller.
        """

        if enc_count % 1 != 0:
            raise ValueError("Encoder count value must be a whole number")

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for encoder count
        """
        params = st.pack('<Hi', channel, enc_count)
        setmsg = Message(message.MGMSG_MOT_SET_ENCCOUNTER, data=params)
        self._send_message(setmsg)

    def encoder_counter(self, channel=1):
        """
        Returns the encoder count in the controller.

        channel specifies the channel to query.

        Example:
          enc_count = con.encoder_counter()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_ENCCOUNTER, param1=channel)
        self._send_message(reqmsg)

        getmsg = self._wait_message(message.MGMSG_MOT_GET_ENCCOUNTER)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for encoder count
        """
        ch, enc_count = st.unpack('<Hi', getmsg.datastring)

        return enc_count

    def start_update_messages(self, update_rate=10):
        """
        Starts automatic production of MGMSG_MOT_GET_DCSTATUSUPDATE messages.
        Based on my testing, update_rate does not influence the number of received messages.
        Anyway, update_rate can be from <0; 255>.

        Worker thread ued for calling keep+alive() method repeatedly every second in order to avoid device timeout
        after 50 messages.
        """

        self._start_alive_worker()
        self.message_listener.message_queue[message.MGMSG_MOT_GET_DCSTATUSUPDATE].change_mode(mode_auto=True)

        reqmsg = Message(message.MGMSG_HW_START_UPDATEMSGS, param1=update_rate)
        self._send_message(reqmsg)

    def _start_alive_worker(self):
        if self._keep_alive_thread is None:
            self._keep_alive_thread = Thread(target=self._keep_alive_worker)
            self._keep_alive_thread.daemon = True
            self._keep_alive_thread.start()
            return True
        return False

    def _keep_alive_worker(self):
        """
        Keep-alive thread - sends keep-alive messages to controller every second until it is requested to stop by main thread.

        Used when automatic update message production is enabled.
        """
        while not self._stop_requested:
            self.keepalive()
            time.sleep(0.5)

    def _stop_alive_worker(self):
        if self._keep_alive_thread is not None:
            self._stop_requested = True
            self._keep_alive_thread.join(timeout=1.0)
            if self._keep_alive_thread.isAlive():
                raise TimeoutException("Attempt to close keep_alive thread timed out! "
                                       "This is most probably because of deadlock => fix the code")
            else:
                self._keep_alive_thread = None
            return True
        return False


    def stop_update_messages(self, wait_ms=1000):
        """
        Stops automatic production of MGMSG_MOT_GET_DCSTATUSUPDATE messages.

        Then, also keep_alive thread is useless and therefore it is stopped.
        """
        reqmsg = Message(message.MGMSG_HW_STOP_UPDATEMSGS)
        self._send_message(reqmsg)

        if self._stop_alive_worker():
            self.message_listener.message_queue[message.MGMSG_MOT_GET_DCSTATUSUPDATE].change_mode(mode_auto=False)

    def _wait_message(self, expected_messageID, timeout_ms=0):
        """
        Waits for message for given timeout amount.
        If timeout is 0 it waits indefinitely.
        """
        if timeout_ms == 0 or timeout_ms is None:
            timeout = None
        else:
            timeout = timeout_ms/float(1000)
        try:
            if expected_messageID in [message.MGMSG_MOT_MOVE_HOMED, message.MGMSG_MOT_MOVE_COMPLETED]:
                    if timeout is not None:
                        endtime = time.time() + timeout
                    partial_timeout = 0.01 if timeout is None else max(timeout/10.0, 0.01)
                    while True:
                        if timeout is not None:
                            remaining = endtime - time.time()
                            if remaining <= 0.0:
                                raise queue.Empty
                        try:
                            return self.message_listener.message_queue[expected_messageID].get(block=True, timeout=partial_timeout)
                        except queue.Empty:
                            pass
                        try:
                            return self.message_listener.message_queue[message.MGMSG_MOT_MOVE_STOPPED].get(block=True, timeout=partial_timeout)
                        except queue.Empty:
                            pass
            return self.message_listener.message_queue[expected_messageID].get(block=True, timeout=timeout)
        except queue.Empty:
            raise TimeoutException("Atttempt to get the message '" + expected_messageID.name  + "' timed out!")

    def _send_message(self, m):
        """
        m should be an instance of Message, or has a pack() method which returns
        bytes to be sent to the controller

        synchronization necessary because of keep_alive() method being called form separate thread
        """
        with self._send_message_lock:
            self._device.write(m.pack())
