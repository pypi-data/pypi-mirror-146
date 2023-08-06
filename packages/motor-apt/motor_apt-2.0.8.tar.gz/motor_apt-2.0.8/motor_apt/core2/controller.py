# -*- coding: utf-8 -*-
"""
Simple class which encapsulate an APT controller
"""
import logging
import time
import struct as st

from motor_apt.core2.message import Message
from motor_apt.core2 import message
from motor_apt.core2.message_device import MessageDevice


class Controller(MessageDevice):
    @property
    def max_velocity(self):
        raise NotImplementedError()

    @property
    def max_acceleration(self):
        raise NotImplementedError()

    @property
    def enccnt(self):
        raise NotImplementedError()

    @property
    def T(self):
        raise NotImplementedError()

    @property
    def position_scale(self):
        # these equations are taken from the APT protocol manual
        return self.enccnt

    @property
    def velocity_scale(self):
        # these equations are taken from the APT protocol manual
        return self.enccnt * self.T * 65536

    @property
    def acceleration_scale(self):
        # these equations are taken from the APT protocol manual
        return self.enccnt * self.T * self.T * 65536

    def open(self):
        super(Controller, self).open()
        self.__resume_end_of_move_messages()

    def status(self, channel=1):
        """
        Returns the status of the controller, which is its position, velocity, and
        statusbits
        Position and velocity will be in mm and mm/s respectively.
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_DCSTATUSUPDATE, param1=channel)
        getmsg = self.query(reqmsg, message.MGMSG_MOT_GET_DCSTATUSUPDATE, timeout=10)
        return ControllerStatus(self, getmsg.datastring)

    def identify(self):
        """
        Flashes the controller's activity LED
        """
        idmsg = Message(message.MGMSG_MOD_IDENTIFY)
        self.send_message(idmsg)

    def reset_parameters(self):
        """
        Resets all parameters to their EEPROM default values.
        IMPORTANT: only one class of controller appear to support this at the
        moment, that being the BPC30x series.
        """
        resetmsg = Message(message.MGMSG_MOT_SET_PZSTAGEPARAMDEFAULTS)
        self.send_message(resetmsg)

    def request_home_params(self):
        reqmsg = Message(message.MGMSG_MOT_REQ_HOMEPARAMS)
        getmsg = self.query(reqmsg, message.MGMSG_MOT_GET_HOMEPARAMS)
        dstr = getmsg.datastring

        """
        <: little endian
        H: 2 bytes for channel id
        H: 2 bytes for home direction
        H: 2 bytes for limit switch
        i: 4 bytes for homing velocity
        i: 4 bytes for offset distance
        """
        return st.unpack('<HHHii', dstr)

    def __suspend_end_of_move_messages(self):
        suspendmsg = Message(message.MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS)
        self.send_message(suspendmsg)

    def __resume_end_of_move_messages(self):
        resumemsg = Message(message.MGMSG_MOT_RESUME_ENDOFMOVEMSGS)
        self.send_message(resumemsg)

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

        abs_pos_apt = int(abs_pos_mm * self.position_scale)

        """
        <: little endian
        H: 2 bytes for channel id
        i: 4 bytes for absolute position
        """
        params = st.pack('<Hi', channel, abs_pos_apt)

        movemsg = Message(message.MGMSG_MOT_MOVE_ABSOLUTE, data=params)

        return self._do_move_msg(movemsg, wait)

    def move_relative(self, dist_mm, channel=1, wait=True):
        """
        Tells the stage to move from its current position the specified
        distance, in mm
        This is currently implemented by getting the current position, then
        computing a new absolute position using dist_mm, then calls
        goto() and returns it returns. Check documentation for goto() for return
        values and such.
        """
        rel_pos_apt = int(round(dist_mm * self.position_scale))

        """
        <: little endian
        H: 2 bytes for channel id
        i: 4 bytes for relative position
        """
        params = st.pack('<Hi', channel, rel_pos_apt)

        movemsg = Message(message.MGMSG_MOT_MOVE_RELATIVE, data=params)
        return self._do_move_msg(movemsg, wait)

    def _do_move_msg(self, movemsg, wait):
        if wait:
            msg = self.query(movemsg, message.MGMSG_MOT_MOVE_COMPLETED)
            sts = ControllerStatus(self, msg.datastring)
            # I find sometimes that after the move completed message there is still
            # some jittering. This aims to wait out the jittering so we are
            # stationary when we return
            while sts.velocity_apt:
                time.sleep(0.01)
                sts = self.status()
            return sts
        else:
            self.send_message(movemsg)
            return None

    def set_velocity_parameters(self, acceleration=None, max_velocity=None, channel=1):
        """
        Sets the trapezoidal velocity parameters of the controller. Note that
        minimum velocity cannot be set, because protocol demands it is always
        zero.
        When called without arguments, max acceleration and max velocity will
        be set to self.max_acceleration and self.max_velocity
        """
        if acceleration is None:
            acceleration = self.max_acceleration

        if max_velocity is None:
            max_velocity = self.max_velocity

        # software limiting again for extra safety
        acceleration = min(acceleration, self.max_acceleration)
        max_velocity = min(max_velocity, self.max_velocity)

        acc_apt = acceleration * self.acceleration_scale
        max_vel_apt = max_velocity * self.velocity_scale

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        """
        params = st.pack('<Hiii', channel, 0, acc_apt, max_vel_apt)
        setmsg = Message(message.MGMSG_MOT_SET_VELPARAMS, data=params)
        self.send_message(setmsg)

    def velocity_parameters(self, channel=1, raw=False):
        """
        Returns the trapezoidal velocity parameters of the controller, that is
        minimum start velocity, acceleration, and maximum velocity. All of which
        are returned in realworld units.
        channel specifies the channel to query.
        raw specifies whether the raw controller values are returned, or the scaled
        real world values. Defaults to False.
        Example:
          min_vel, acc, max_vel = con.velocity_parameters()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_VELPARAMS, param1=channel)

        getmsg = self.query(reqmsg, message.MGMSG_MOT_GET_VELPARAMS)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        """
        ch, min_vel, acc, max_vel = st.unpack('<Hiii', getmsg.datastring)

        if not raw:
            min_vel /= self.velocity_scale
            max_vel /= self.velocity_scale
            acc /= self.acceleration_scale

        return min_vel, acc, max_vel

    def info(self):
        """
        Gets hardware info of the controller, returned as a tuple containing:
          - serial number
          - model number
          - hardware type, either 45 for multi-channel motherboard, or 44 for
            brushless DC motor
          - firmware version as major.interim.minor
          - notes
          - hardware version number
          - modification state of controller
          - number of channels
        """

        reqmsg = Message(message.MGMSG_HW_REQ_INFO)

        getmsg = self.query(reqmsg, message.MGMSG_HW_GET_INFO)
        """
        <: small endian
        I:    4 bytes for serial number
        8s:   8 bytes for model number
        H:    2 bytes for hw type
        4s:   4 bytes for firmware version
        48s:  48 bytes for notes
        12s:  12 bytes of empty space
        H:    2 bytes for hw version
        H:    2 bytes for modificiation state
        H:    2 bytes for number of channels
        """
        info = st.unpack('<I8sH4s48s12sHHH', getmsg.datastring)

        sn, model, hwtype, fwver, notes, _, hwver, modstate, numchan = info

        fwverminor = ord(fwver[0])
        fwverinterim = ord(fwver[1])
        fwvermajor = ord(fwver[2])

        fwver = '%d.%d.%d' % (fwvermajor, fwverinterim, fwverminor)

        return sn, model, hwtype, fwver, notes, hwver, modstate, numchan

    def stop(self, channel=1, immediate=False, wait=True):
        """
        Stops the motor on the specified channel. If immediate is True, then the
        motor stops immediately, otherwise it stops in a profiled manner, i.e.
        decelerates accoding to max acceleration from current velocity down to zero
        If wait is True, then this method returns only when MGMSG_MOT_MOVE_STOPPED
        is read, and controller reports velocity of 0.
        This method returns an instance of ControllerStatus if wait is True, None
        otherwise.
        """
        stopmsg = Message(message.MGMSG_MOT_MOVE_STOP,
                          param1=channel,
                          param2=int(immediate))
        if wait:
            msg = self.query(stopmsg, message.MGMSG_MOT_MOVE_STOPPED, timeout=2)
            if msg:
                sts = ControllerStatus(self, msg.datastring)
                # I find sometimes that after the move completed message there is still
                # some jittering. This aims to wait out the jittering so we are
                # stationary when we return
                while sts.velocity_apt:
                    time.sleep(0.01)
                    sts = self.status()
                return sts
        else:
            self.send_message(stopmsg)
            return None

    def _pump_loop_hook(self):
        self.keepalive()

    def keepalive(self):
        """
        This sends MGMSG_MOT_ACK_DCSTATUSUPDATE to the controller to keep it
        from going dark.
        Per documentation:
          If using the USB port, this message called "server alive" must be sent
          by the server to the controller at least once a second or the controller
          will stop responding after ~50 commands
        """
        msg = Message(message.MGMSG_MOT_ACK_DCSTATUSUPDATE)
        self.send_message(msg)

    def jog(self, channel=1, direction=2, wait=True):
        """
        channel always 1 for TDC001
        direction 1 or 2
            - real direction stage-dependent
            - for CR1/M-Z7: CCW=1 CW=2

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message
        constructor

        WARNING: wait=True and jog_mode=1 (continuous) results in infinite loop!
        """

        if direction not in [1, 2]:
            raise ValueError("Allowed values for direction are only 1 (forward) and 2 (backward)!")

        movemsg = Message(message.MGMSG_MOT_MOVE_JOG, param1=channel, param2=direction)

        return self._do_move_msg(movemsg, wait)

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
        self.send_message(setmsg)

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
        getmsg = self.query(reqmsg, message.MGMSG_MOT_GET_JOGPARAMS)

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
        self.send_message(setmsg)

    def encoder_counter(self, channel=1):
        """
        Returns the encoder count in the controller.

        channel specifies the channel to query.

        Example:
          enc_count = con.encoder_counter()
        """
        reqmsg = Message(message.MGMSG_MOT_REQ_ENCCOUNTER, param1=channel)
        getmsg = self.query(reqmsg, message.MGMSG_MOT_GET_ENCCOUNTER)

        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for encoder count
        """
        ch, enc_count = st.unpack('<Hi', getmsg.datastring)

        return enc_count

    def __repr__(self):
        return 'Controller(serial=%s, device=%s)' % (self.serial_number, self._device)


class ControllerStatus(object):
    """
    This class encapsulate the controller status, which includes its position,
    velocity, and various flags.
    The position and velocity properties will return realworld values of
    mm and mm/s respectively.
    """

    def __init__(self, controller, statusbytestring):
        """
        Construct an instance of ControllerStatus from the 14 byte status sent by
        the controller which contains the current position encoder count, the
        actual velocity, scaled, and statusbits.
        """

        super(ControllerStatus, self).__init__()

        """
        <: little endian
        H: 2 bytes for channel ID
        i: 4 bytes for position counter
        h: 2 bytes for velocity
        H: 2 bytes reserved
        I: 4 bytes for status
        Note that velocity in the docs is stated as a unsigned word, by in reality
        it looks like it is signed.
        """
        channel, pos_apt, vel_apt, _, statusbits = st.unpack('<HihHI',
                                                             statusbytestring)

        self.channel = channel
        if pos_apt:
            self.position = float(pos_apt) / controller.position_scale
        else:
            self.position = 0

        # XXX the protocol document, revision 7, is explicit about the scaling
        # Note that I don't trust this value, because the measured velocity
        # does not correspond to the value from the scaling. The value used here
        # is derived from trial and error
        if vel_apt:
            self.velocity = float(vel_apt) / 10
        else:
            self.velocity = 0

        self.statusbits = statusbits

        # save the "raw" controller values since they are convenient for
        # zero-checking
        self.position_apt = pos_apt
        self.position_scale = controller.position_scale
        self.velocity_apt = vel_apt

    @property
    def forward_hardware_limit_switch_active(self):
        return self.statusbits & 0x01

    @property
    def reverse_hardware_limit_switch_active(self):
        return self.statusbits & 0x02

    @property
    def moving(self):
        return self.moving_forward or self.moving_reverse

    @property
    def moving_forward(self):
        return self.statusbits & 0x10

    @property
    def moving_reverse(self):
        return self.statusbits & 0x20

    @property
    def jogging_forward(self):
        return self.statusbits & 0x40

    @property
    def jogging_reverse(self):
        return self.statusbits & 0x80

    @property
    def homing(self):
        return self.statusbits & 0x200

    @property
    def homed(self):
        return self.statusbits & 0x400

    @property
    def tracking(self):
        return self.statusbits & 0x1000

    @property
    def settled(self):
        return self.statusbits & 0x2000

    @property
    def excessive_position_error(self):
        """
        This flag means that there is excessive positioning error, and
        the stage should be re-homed. This happens if while moving the stage
        is impeded, and where it thinks it is isn't where it is
        """
        return self.statusbits & 0x4000

    @property
    def motor_current_limit_reached(self):
        return self.statusbits & 0x01000000

    @property
    def channel_enabled(self):
        return self.statusbits & 0x80000000

    @property
    def shortstatus(self):
        """
        Returns a short, fixed width, status line that shows whether the
        controller is moving, the direction, whether it has been homed, and
        whether excessive position error is present.
        These are shown via the following letters:
          H: homed
          M: moving
          T: tracking
          S: settled
          F: forward limit switch tripped
          R: reverse limit switch tripped
          E: excessive position error
        Format of the string is as follows:
          H MTS FRE
        Each letter may or may not be present.  When a letter is present, it is a
        positive indication of the condition.
        e.g.
        "H M-- ---" means homed, moving
        "H M-- --E" means homed, moving reverse, excessive position error
        """
        shortstat = []

        def add(flag, letter):
            if flag:
                shortstat.append(letter)
            else:
                shortstat.append('-')

        sep = ' '
        add(self.homed, 'H')

        shortstat.append(sep)

        add(self.moving, 'M')
        add(self.tracking, 'T')
        add(self.settled, 'S')

        shortstat.append(sep)

        add(self.forward_hardware_limit_switch_active, 'F')
        add(self.reverse_hardware_limit_switch_active, 'R')
        add(self.excessive_position_error, 'E')

        return ''.join(shortstat)

    def flag_strings(self):
        """
        Returns the various flags as user readable strings
        """
        """
        XXX Breaking the DRY principle here, but this is so much more compact!
        """
        masks = {0x01: 'Forward hardware limit switch active',
                 0x02: 'Reverse hardware limit switch active',
                 0x10: 'In motion, moving forward',
                 0x20: 'In motion, moving backward',
                 0x40: 'In motion, jogging forward',
                 0x80: 'In motion, jogging backward',
                 0x200: 'In motion, homing',
                 0x400: 'Homed',
                 0x1000: 'Tracking',
                 0x2000: 'Settled',
                 0x4000: 'Excessive position error',
                 0x01000000: 'Motor current limit reached',
                 0x80000000: 'Channel enabled'
                 }
        statuslist = []
        for bitmask in masks:
            if self.statusbits & bitmask:
                statuslist.append(masks[bitmask])

        return statuslist

    def __str__(self):
        return 'pos=%.2fmm vel=%.2fmm/s, flags=%s' % (self.position, self.velocity, self.flag_strings())
