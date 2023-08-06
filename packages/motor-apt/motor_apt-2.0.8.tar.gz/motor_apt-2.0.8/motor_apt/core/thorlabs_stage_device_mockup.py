# -*- coding: utf-8 -*-
"""
Created on 03.06.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
from abc import ABCMeta, abstractproperty
import numbers
import struct as st
from random import randint
import threading
import time
import sys
import logging

from pylibftdi import FLUSH_BOTH, FLUSH_INPUT, FLUSH_OUTPUT
from enum import Enum

from motor_apt.core.pyAPT import message
from motor_apt.core.pyAPT.message import Message
from motor_apt.core.ftdi_device_mockup import FtdiDeviceMockup
from motor_apt.core.timeout_exception import TimeoutException


class ThorlabsStageDeviceMockup(FtdiDeviceMockup, metaclass=ABCMeta):

    def __init__(self, device_id="Thorlabs APT_Device Mockup", mode="b", encoding="latin1", lazy_open=False,
                 sn=None, model="MOCKUP00", hw_type=0, fw_version="1.0.0", notes="", hw_version=0, mod_state=0, channels_list=[]):
        self._message_buffer = ''
        self._message_method_bindings = self._define_message_method_bindings()

        if sn is None:
            sn = randint(0, 99999999)
        else:
            if not isinstance(sn, numbers.Integral) or sn / 100000000 != 0:
                raise ValueError("sn must be positive number with maximum of 8 digits")
        self._sn = sn

        if not isinstance(model, str) or len(model) > 8:
            raise ValueError("model must be string of maximum length equal to 8")
        self._model = model

        if not isinstance(hw_type, numbers.Integral) or hw_type / 65536 != 0:
            raise ValueError("hw_type must be positive number lower than 65536")
        self._hw_type = hw_type

        if not isinstance(fw_version, str):
            raise ValueError("fw_version must be string in format major.interim.minor, e.g. 1.0.8")
        versions = fw_version.split('.')
        if len(versions) > 3:
            raise ValueError("fw_version must be string in format major.interim.minor, e.g. 1.0.8")
        versions_int = [int(version)for version in versions]
        versions_int.reverse()
        versions_int.append(0)
        self._fw_version = str(bytearray(versions_int))

        if not isinstance(notes, str) or len(notes) > 48:
            raise ValueError("notes must be string at most 48 characters long")
        self._notes = notes

        if not isinstance(hw_version, numbers.Integral) or hw_version / 65536 != 0:
            raise ValueError("hw_version must be positive number lower than 65536")
        self._hw_version = hw_version

        if not isinstance(mod_state, numbers.Integral) or mod_state / 65536 != 0:
            raise ValueError("mod_state must be positive number lower than 65536")
        self._mod_state = mod_state

        if not isinstance(channels_list, list) or len(channels_list) not in range(1, 65536):
            raise ValueError("channels_list must be list of Channel objects (at least 1 required, maximum 65535")
        for channel in channels_list:
            if not isinstance(channel, Channel):
                raise ValueError("channels_list must be list of Channel objects (at least 1 required, maximum 65535")
        self._no_of_channels = len(channels_list)
        self._channels = {}
        for i in range(1, self._no_of_channels + 1):
            self._channels[i] = channels_list[i-1]

        self._suspend_end_of_move_messages = False
        self._disconnected = False

        self._buffer_access_lock = threading.Lock()

        self._status_udates_counter = 0
        self._status_udates_thread_stop_requested = False
        self._status_udates_thread = None

        super(ThorlabsStageDeviceMockup, self).__init__(device_id, mode, encoding, lazy_open)

    def _start_status_updates_thread(self):
        self._status_udates_counter = 0
        self._status_udates_thread_stop_requested = False
        self._status_udates_thread = threading.Thread(target=self._status_updates_worker)
        self._status_udates_thread.daemon = True
        self._status_udates_thread.start()

    def _status_updates_worker(self):
        while not self._status_udates_thread_stop_requested:
            time.sleep(0.05)
            if self._status_udates_counter < 50:
                for id in self._channels:
                    params = st.pack('<HihHI', self._channels[id].id, self._channels[id].position_counter, self._channels[id].actual_velocity, 0, self._channels[id].status)
                    self._push_return_msg_on_buffer(Message(message.MGMSG_MOT_GET_DCSTATUSUPDATE, data=params))
                    self._status_udates_counter += 1
                    if self._status_udates_counter == 50:
                        break

    def _stop_status_updates_thread(self, wait_ms=1000):
        """
        Stops status update thread.
        First signals worker thread that it should finish, then waits for it for given timeout. If thread is not done
        after given timeout, an timeout exception is thrown.
        """
        if self._status_udates_thread is not None and self._status_udates_thread.isAlive():
            self._status_udates_thread_stop_requested = True
            self._status_udates_thread.join(timeout=wait_ms/float(1000))
            if self._status_udates_thread.isAlive():
                raise TimeoutException("Attempt to close status updates thread timed out!")
            else:
                self._status_udates_thread = None

    def _define_message_method_bindings(self):
        result = {}
        for mess in message:
            method_candidate_name = "_" + mess.name + "_handler"
            if hasattr(self, method_candidate_name):
                result[mess] = getattr(self, method_candidate_name)
            else:
                def create_unhandled_message_hadler(msg):
                    def f(param1=0, param2=0, datastring=None):
                        raise NotImplementedError(self.device_id + ': Handler for the message "' + msg.name + '" was not defined!')
                    return f
                result[mess] = create_unhandled_message_hadler(mess)
        return result

    def _on_read(self, length):
        if not self._disconnected:
            with self._buffer_access_lock:
                length = min(length, len(self._message_buffer))
                byte_data = self._message_buffer[:length]
                self._message_buffer = self._message_buffer[length:]
            return byte_data
        else:
            return ''

    def _on_write(self, byte_data):
        data_str = None
        header_data = byte_data[: message.MGMSG_HEADER_SIZE]
        msg = Message.unpack(header_data, header_only=True)
        if msg.hasdata:
          data = byte_data[message.MGMSG_HEADER_SIZE: message.MGMSG_HEADER_SIZE + msg.datalength]
          msglist = list(msg)
          msglist[-1] = data
          msg = Message._make(msglist)
          data_str = msg.datastring

        ret_msg = self._message_method_bindings[msg.messageID](msg.param1, msg.param2, data_str)
        return self._push_return_msg_on_buffer(ret_msg)

    def _push_return_msg_on_buffer(self, ret_msg):
        if not self._disconnected:
            if isinstance(ret_msg, Message):
                packed_msg = ret_msg.pack()
                with self._buffer_access_lock:
                    self._message_buffer += packed_msg
                return len(packed_msg)
            elif ret_msg is None:
                return 0
            else:
                raise ValueError("handler methods can return only None or Message type")
        else:
            return 0

    def flush(self, flush_what=FLUSH_BOTH):
        """
        Instruct the FTDI device to flush its FIFO buffers

        By default both the input and output buffers will be
        flushed, but the caller can selectively chose to only
        flush the input or output buffers using `flush_what`:

        :param flush_what: select what to flush:
            `FLUSH_BOTH` (default);
            `FLUSH_INPUT` (just the rx buffer);
            `FLUSH_OUTPUT` (just the tx buffer)
        """
        raise NotImplementedError("TODO")

    def close(self):
        super(ThorlabsStageDeviceMockup, self).close()
        self._stop_status_updates_thread()
        for channel_id in self._channels:
            self._channels[channel_id].stop()

    def _MGMSG_MOT_SET_ENCCOUNTER_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for encoder count
        """
        logging.debug("MGMSG_MOT_SET_ENCCOUNTER")
        ch, enc_count = st.unpack('<Hi', datastring)
        if ch not in self._channels:
            return
        with self._channels[ch]._moving_lock:
            self._channels[ch].encoder_counter = enc_count
            self._channels[ch]._moving_thread_target = enc_count
            self._channels[ch].status &= 0xFFFFF0FF
            self._channels[ch].status |= 0x100

    def _MGMSG_MOT_RESUME_ENDOFMOVEMSGS_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_MOT_RESUME_ENDOFMOVEMSGS")
        self._suspend_end_of_move_messages = False

    def _MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS")
        self._suspend_end_of_move_messages = True

    def _MGMSG_MOT_REQ_DCSTATUSUPDATE_handler(self, param1=0, param2=0, datastring=None):
        """
        <: little endian
        H: 2 bytes for channel ID
        i: 4 bytes for position counter
        H: 2 bytes for velocity
        H: 2 bytes reserved
        I: 4 bytes for status

        Note that velocity in the docs is stated as a unsigned word, by in reality
        it looks like it is signed.
        """
        logging.debug("MGMSG_MOT_REQ_DCSTATUSUPDATE")
        if param1 not in self._channels:
            return
        params = st.pack('<HihHI', param1, self._channels[param1].position_counter, self._channels[param1].actual_velocity, 0, self._channels[param1].status)
        return Message(message.MGMSG_MOT_GET_DCSTATUSUPDATE, data=params)

    def _MGMSG_HW_START_UPDATEMSGS_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_HW_START_UPDATEMSGS")
        self._start_status_updates_thread()

    def _MGMSG_MOT_ACK_DCSTATUSUPDATE_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_MOT_ACK_DCSTATUSUPDATE")
        self._status_udates_counter = 0

    def _MGMSG_HW_STOP_UPDATEMSGS_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_HW_STOP_UPDATEMSGS")
        self._stop_status_updates_thread()

    def _MGMSG_MOT_REQ_ENCCOUNTER_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for encoder count
        """
        logging.debug("MGMSG_MOT_REQ_ENCCOUNTER")
        if param1 not in self._channels:
            return
        with self._channels[param1]._moving_lock:
            params = st.pack('<Hi', param1, self._channels[param1].encoder_counter)
            return Message(message.MGMSG_MOT_GET_ENCCOUNTER, data=params)

    def _MGMSG_MOD_IDENTIFY_handler(self, param1=0, param2=0, datastring=None):
        logging.debug("MGMSG_MOD_IDENTIFY")

    def _MGMSG_HW_REQ_INFO_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_HW_REQ_INFO")
        params = st.pack('<I8sH4s48s12sHHH', self._sn, self._model, self._hw_type, self._fw_version, self._notes, '', self._hw_version, self._mod_state, self._no_of_channels)
        return Message(message.MGMSG_HW_GET_INFO, data=params)

    def _MGMSG_MOT_SET_POSCOUNTER_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for position
        """
        logging.debug("MGMSG_MOT_SET_POSCOUNTER")
        ch, position = st.unpack('<Hi', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].position_counter = position
        self._channels[ch].status &= 0xFFFFF0FF
        self._channels[ch].status |= 0x100

    def _MGMSG_MOT_REQ_POSCOUNTER_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for position
        """
        logging.debug("MGMSG_MOT_REQ_POSCOUNTER")
        if param1 not in self._channels:
            return
        params = st.pack('<Hi', param1, self._channels[param1].position_counter)
        return Message(message.MGMSG_MOT_GET_POSCOUNTER, data=params)

    def _MGMSG_MOT_SET_VELPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        """
        logging.debug("MGMSG_MOT_SET_VELPARAMS")
        ch,min_vel,acc,max_vel = st.unpack('<Hiii', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].move_target_acceleration = acc
        self._channels[ch].move_target_velocity = max_vel

    def _MGMSG_MOT_REQ_VELPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for min velocity
        i: 4 bytes for acceleration
        i: 4 bytes for max velocity
        """
        logging.debug("MGMSG_MOT_REQ_VELPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<Hiii', param1, self._channels[param1].minimum_velocity, self._channels[param1].move_target_acceleration, self._channels[param1].move_target_velocity)
        return Message(message.MGMSG_MOT_GET_VELPARAMS, data=params)

    def _MGMSG_MOT_SET_JOGPARAMS_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_MOT_SET_JOGPARAMS")
        ch, jog_mode, step_size, min_vel, acc, max_vel, stop_mode = st.unpack('<HHiiiiH', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].jog_mode = jog_mode
        self._channels[ch].jog_step_size = step_size
        self._channels[ch].jog_target_acceleration = acc
        self._channels[ch].jog_target_velocity = max_vel
        self._channels[ch].jog_stop_mode = stop_mode

    def _MGMSG_MOT_REQ_JOGPARAMS_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_MOT_REQ_JOGPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<HHiiiiH', param1, self._channels[param1].jog_mode, self._channels[param1].jog_step_size,
                         self._channels[param1].minimum_velocity, self._channels[param1].jog_target_acceleration,
                         self._channels[param1].jog_target_velocity, self._channels[param1].jog_stop_mode)
        return Message(message.MGMSG_MOT_GET_JOGPARAMS, data=params)

    def _MGMSG_MOT_SET_GENMOVEPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for backlash distance
        """
        logging.debug("MGMSG_MOT_SET_GENMOVEPARAMS")
        ch, backlash_distance = st.unpack('<Hi', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].backlash_distance = backlash_distance

    def _MGMSG_MOT_REQ_GENMOVEPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for backlash distance
        """
        logging.debug("MGMSG_MOT_REQ_GENMOVEPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<Hi', param1, self._channels[param1].backlash_distance)
        return Message(message.MGMSG_MOT_GET_GENMOVEPARAMS, data=params)

    def _MGMSG_MOT_SET_LIMSWITCHPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for CW hard limit
        H: 2 bytes for CCW hard limit
        i: 4 bytes for CW soft limit (not applicable to TDC001)
        i: 4 bytes for CCW soft limit (not applicable to TDC001)
        H: 2 bytes for soft limit mode (not applicable to TDC001)
        """
        logging.debug("MGMSG_MOT_SET_LIMSWITCHPARAMS")
        ch, cw_hard, ccw_hard, cw_soft, ccw_soft, soft_mode = st.unpack('<HHHiiH', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].switch_cw_hard = cw_hard
        self._channels[ch].switch_ccw_hard = ccw_hard
        self._channels[ch].switch_cw_soft = cw_soft
        self._channels[ch].switch_ccw_soft = ccw_soft
        self._channels[ch].switch_soft_mode = soft_mode

    def _MGMSG_MOT_REQ_LIMSWITCHPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        H: 2 bytes for CW hard limit
        H: 2 bytes for CCW hard limit
        i: 4 bytes for CW soft limit (not applicable to TDC001)
        i: 4 bytes for CCW soft limit (not applicable to TDC001)
        H: 2 bytes for soft limit mode (not applicable to TDC001)
        """
        logging.debug("MGMSG_MOT_REQ_LIMSWITCHPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<HHHiiH', param1, self._channels[param1].switch_cw_hard, self._channels[param1].switch_ccw_hard,
                         self._channels[param1].switch_cw_soft, self._channels[param1].switch_ccw_soft, self._channels[param1].switch_soft_mode)
        return Message(message.MGMSG_MOT_GET_LIMSWITCHPARAMS, data=params)

    def _MGMSG_MOT_SET_DCPIDPARAMS_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_MOT_SET_DCPIDPARAMS")
        ch, proportional_gain, integral_gain, differential_gain, integral_limit, filter_control = st.unpack('<HiiiiH', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].pid_proportional_gain = proportional_gain
        self._channels[ch].pid_integral_gain = integral_gain
        self._channels[ch].pid_differential_gain = differential_gain
        self._channels[ch].pid_integral_limit = integral_limit
        self._channels[ch].pid_filter_control = filter_control

    def _MGMSG_MOT_REQ_DCPIDPARAMS_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_MOT_REQ_DCPIDPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<HiiiiH', param1, self._channels[param1].pid_proportional_gain, self._channels[param1].pid_integral_gain,
                         self._channels[param1].pid_differential_gain, self._channels[param1].pid_integral_limit,
                         self._channels[param1].pid_filter_control)
        return Message(message.MGMSG_MOT_GET_DCPIDPARAMS, data=params)

    def _MGMSG_MOT_MOVE_RELATIVE_handler(self, param1=0, param2=0, datastring=None):
        """
        <: little endian
        H: 2 bytes for channel id
        i: 4 bytes for relative position
        """
        logging.debug("MGMSG_MOT_MOVE_RELATIVE")
        ch, rel_pos = st.unpack('<Hi', datastring)
        if ch not in self._channels:
            return
        with self._channels[ch]._moving_lock:
            self._channels[ch].current_movement_type = Channel.MovementType.Moving
            self._channels[ch]._moving_thread_target = self._channels[ch].encoder_counter + rel_pos

    def _MGMSG_MOT_MOVE_ABSOLUTE_handler(self, param1=0, param2=0, datastring=None):
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
        logging.debug("MGMSG_MOT_MOVE_ABSOLUTE")
        ch, abs_pos = st.unpack('<Hi', datastring)
        if ch not in self._channels:
            return
        with self._channels[ch]._moving_lock:
            self._channels[ch].current_movement_type = Channel.MovementType.Moving
            self._channels[ch]._moving_thread_target = abs_pos

    def _MGMSG_MOT_MOVE_VELOCITY_handler(self, param1=0, param2=0, datastring=None):
        """
        Tells the stage to move continuously in selected direction.

        direction = 1 => forward movement
        direction = 2 => backward movement

        Moves until either a stop command is called, or a limit switch is reached.

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor
        """
        logging.debug("MGMSG_MOT_MOVE_VELOCITY")
        if param1 not in self._channels:
            return
        if param2 not in [1,2]:
            return
        with self._channels[param1]._moving_lock:
            self._channels[param1].current_movement_type = Channel.MovementType.Moving
            self._channels[param1]._moving_thread_target = (-1 if param2 == 2 else 1) * sys.maxsize - (1 if param2 == 2
                                                                                                       else 0)

    def _MGMSG_MOT_SET_HOMEPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: little endian
        H: 2 bytes for channel id
        H: 2 bytes for home direction; 1 || 2
        H: 2 bytes for limit switch
        i: 4 bytes for homing velocity
        i: 4 bytes for offset distance
        """
        logging.debug("MGMSG_MOT_SET_HOMEPARAMS")
        ch, direction, limit_switch, velocity, offset = st.unpack('<HHHii', datastring)
        if ch not in self._channels:
            return
        self._channels[ch].homing_direction = direction
        self._channels[ch].homing_limit_switch = limit_switch
        self._channels[ch].homing_velocity = velocity
        self._channels[ch].homing_offset = offset
        self._channels[ch].status &= 0xFFFFF0FF
        self._channels[ch].status |= 0x100

    def _MGMSG_MOT_REQ_HOMEPARAMS_handler(self, param1=0, param2=0, datastring=None):
        """
        <: little endian
        H: 2 bytes for channel id
        H: 2 bytes for home direction; 1 = forward; 2 = reverse
        H: 2 bytes for limit switch; 1 || 4 for CR1
        i: 4 bytes for homing velocity
        i: 4 bytes for offset distance
        """
        logging.debug("MGMSG_MOT_REQ_HOMEPARAMS")
        if param1 not in self._channels:
            return
        params = st.pack('<HHHii', param1, self._channels[param1].homing_direction, self._channels[param1].homing_limit_switch, self._channels[param1].homing_velocity, self._channels[param1].homing_offset)
        return Message(message.MGMSG_MOT_GET_HOMEPARAMS, data=params)

    def _MGMSG_MOT_MOVE_HOME_handler(self, param1=0, param2=0, datastring=None):
        """
        Moves the stage to home position.

        channel always 1 for TDC001

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor
        """
        logging.debug("MGMSG_MOT_MOVE_HOME")
        if param1 not in self._channels:
            return
        with self._channels[param1]._moving_lock:
            self._channels[param1].current_movement_type = Channel.MovementType.Homing
            if self._channels[param1].homing_direction == 2:
                self._channels[param1]._moving_thread_target = self._channels[param1].real_position_min
            elif self._channels[param1].homing_direction == 1:
                self._channels[param1]._moving_thread_target = self._channels[param1].real_position_max

    def _MGMSG_MOT_MOVE_JOG_handler(self, param1=0, param2=0, datastring=None):
        """
        channel always 1 for TDC001
        direction 1 or 2
            - real direction stage-dependent
            - for CR1/M-Z7: CCW=1 CW=2

        packing not necessary as this is header-only message => param1 and param2 used instead of data in Message constructor

        WARNING: wait=True and jog_mode=1 (continuous) results in infinite loop!
        """
        logging.debug("MGMSG_MOT_MOVE_JOG")
        if param1 not in self._channels:
            return
        if param2 not in [1,2]:
            return
        with self._channels[param1]._moving_lock:
            self._channels[param1].current_movement_type = Channel.MovementType.Jogging
            self._channels[param1]._moving_thread_target = self._channels[param1].encoder_counter + (-1 if param2 == 1 else 1) * self._channels[param1].jog_step_size

    def _MGMSG_MOT_MOVE_STOP_handler(self, param1=0, param2=0, datastring=None):
        """
        Stops the motor on the specified channel. If immediate is True, then the
        motor stops immediately, otherwise it stops in a profiled manner, i.e.
        decelerates according to max acceleration from current velocity down to zero

        If wait is True, then this method returns only when MGMSG_MOT_MOVE_STOPPED
        is read, and controller reports velocity of 0.

        This method returns an instance of ControllerStatus if wait is True, None
        otherwise.
        """
        logging.debug("MGMSG_MOT_MOVE_STOP")
        if param1 not in self._channels:
            return
        if param2 not in [1,2]:
            return
        with self._channels[param1]._moving_lock:
            if self._channels[param1]._moving_thread_target != self._channels[param1].encoder_counter:
                self._channels[param1]._moving_thread_target = self._channels[param1].encoder_counter
                self._channels[param1].current_movement_type = Channel.MovementType.No
                if (self._channels[param1].status & 0x00000F00) >> 8 == 2:
                    self._channels[param1].status &= 0xFFFFF0FF
                    self._channels[param1].status |= 0x100
                if not self._suspend_end_of_move_messages:
                    logging.debug("MGMSG_MOT_MOVE_STOPPED")
                    params = st.pack('<HihHI', param1, self._channels[param1].position_counter, self._channels[param1].actual_velocity, 0, self._channels[param1].status)
                    return Message(message.MGMSG_MOT_MOVE_STOPPED, data=params)

    def _MGMSG_HW_DISCONNECT_handler(self, param1=0, param2=0, datastring=None):
        """
        Sent by the hardware unit or host when either wants to disconnect from the Ethernet/USB bus.
        """
        logging.debug("MGMSG_HW_DISCONNECT")
        # self._disconnected = True


class Channel(object):
    class MovementType(Enum):
        No = 0
        Moving = 1
        Jogging = 2
        Homing = 3

    def __init__(self, id, controller, position_scale, acceleration_scale, maximum_acceleration, velocity_scale, maximum_velocity, encoder_counter=0, position_counter=None,
                 real_position_min=None, real_position_max=None,  # cw_limit_real_position= None, ccw_limit_real_position=None,
                 status=0x80000100, current_movement_type=MovementType.No, actual_velocity = 0, move_target_velocity=None, jog_target_velocity=None,
                 move_target_acceleration=None, jog_target_acceleration=None,
                 jog_mode=2, jog_step_size=1, jog_stop_mode=2,
                 backlash_distance = 0,
                 switch_cw_hard=1, switch_ccw_hard=1, switch_cw_soft=0, switch_ccw_soft=0, switch_soft_mode=1,
                 pid_proportional_gain = 0, pid_integral_gain=0, pid_differential_gain=0, pid_integral_limit=0, pid_filter_control=0x0F,
                 homing_direction=2, homing_limit_switch=1, homing_velocity=None, homing_distance_offset=0):
        self.id = id
        self.parent_controller = controller
        self.status = status
        self.encoder_counter = encoder_counter
        self.position_counter = (position_counter * position_scale) if position_counter is not None else encoder_counter
        if self.position_counter != self.encoder_counter:
            raise ValueError("Values of position counter and encoder counter are inconsistent!")
        # self.real_position = real_position * position_scale
        self.real_position_min = (real_position_min * position_scale) if real_position_min is not None else -sys.maxsize - 1
        if self.encoder_counter < self.real_position_min:
            raise ValueError("Value of encoder count can't be lower than minimal position!")
        elif self.encoder_counter == self.real_position_min:
            self.status &= 0xFFFFFFF0
            self.status |= 0x1
        self.real_position_max = (real_position_max * position_scale) if real_position_max is not None else sys.maxsize
        if self.encoder_counter > self.real_position_max:
            raise ValueError("Value of encoder count can't be higher than maximal position!")
        elif self.encoder_counter == self.real_position_max:
            self.status &= 0xFFFFFFF0
            self.status |= 0x2
        # self.cw_limit_real_position = (cw_limit_real_position * position_scale) if cw_limit_real_position is not None else self.real_position_min
        # self.ccw_limit_real_position = (ccw_limit_real_position * position_scale) if ccw_limit_real_position is not None else self.real_position_max


        self.current_movement_type = current_movement_type

        self.actual_velocity = actual_velocity * velocity_scale
        self.move_target_velocity = (move_target_velocity if move_target_velocity is not None else maximum_velocity) * velocity_scale
        self.jog_target_velocity = (jog_target_velocity if jog_target_velocity is not None else maximum_velocity) * velocity_scale
        self.maximum_velocity = maximum_velocity * velocity_scale

        self.move_target_acceleration = (move_target_acceleration if move_target_acceleration is not None else maximum_acceleration) * acceleration_scale
        self.jog_target_acceleration = (jog_target_acceleration if jog_target_acceleration is not None else maximum_acceleration) * acceleration_scale
        self.maximum_acceleration = maximum_acceleration * acceleration_scale

        self.jog_mode = jog_mode
        self.jog_step_size = jog_step_size * position_scale
        self.jog_stop_mode = jog_stop_mode

        self.backlash_distance = backlash_distance * position_scale

        self.switch_cw_hard = switch_cw_hard
        self.switch_ccw_hard = switch_ccw_hard
        self.switch_cw_soft = switch_cw_soft
        self.switch_ccw_soft = switch_ccw_soft
        self.switch_soft_mode = switch_soft_mode

        self.pid_proportional_gain = pid_proportional_gain
        self.pid_integral_gain = pid_integral_gain
        self.pid_differential_gain = pid_differential_gain
        self.pid_integral_limit = pid_integral_limit
        self.pid_filter_control = pid_filter_control

        self.homing_direction = homing_direction
        self.homing_limit_switch = homing_limit_switch
        self.homing_velocity = homing_velocity if homing_velocity is not None else maximum_velocity * velocity_scale
        self.homing_distance_offset = homing_distance_offset * position_scale

        self.position_scale = position_scale
        self.acceleration_scale = acceleration_scale
        self.velocity_scale = velocity_scale

        self.velocity_dict = {}
        self.velocity_dict[Channel.MovementType.Moving] = self.move_target_velocity
        self.velocity_dict[Channel.MovementType.Jogging] = self.jog_target_velocity
        self.velocity_dict[Channel.MovementType.Homing] = self.homing_velocity

        self._moving_lock = threading.Lock()

        self._moving_thread_stop_requested = False
        self._moving_thread_target = 0
        self._moving_thread = threading.Thread(target=self._moving_worker)
        self._moving_thread.daemon = True
        self._moving_thread.start()

    @property
    def minimum_velocity(self):
        return 0

    def _moving_worker(self):
        while not self._moving_thread_stop_requested:
            time_step = 0.05
            time.sleep(time_step)
            with self._moving_lock:
                if self._moving_thread_target != self.encoder_counter:
                    actual_velocity = min(self.maximum_velocity, self.velocity_dict[self.current_movement_type])
                    self.actual_velocity = actual_velocity / self.velocity_scale  # human readable value
                    step = actual_velocity * self.position_scale / self.velocity_scale * time_step
                    remaining = self._moving_thread_target - self.encoder_counter
                    real_step = min(step, abs(remaining)) * (-1 if remaining < 0 else 1)
                    self.encoder_counter += real_step
                    self.position_counter = self.encoder_counter
                    if self.current_movement_type is Channel.MovementType.Jogging:
                        self.status &= 0xFFFFFF0F
                        self.status |= 0x40 if real_step > 0 else 0x80
                    elif self.current_movement_type in [Channel.MovementType.Moving, Channel.MovementType.Homing]:
                        self.status &= 0xFFFFFF0F
                        self.status |= 0x10 if real_step > 0 else 0x20
                    elif self.current_movement_type is Channel.MovementType.No:
                        self._moving_thread_target = self.encoder_counter
                    elif self.current_movement_type is not Channel.MovementType.Homing:
                        raise NotImplementedError("Logic for " + str(self.current_movement_type) + " was not implemented")
                    if self.current_movement_type is Channel.MovementType.Homing:
                        self.status &= 0xFFFFF0FF
                        self.status |= 0x200
                    self.status &= 0xFFFFFFF0

                    if self.encoder_counter < self.real_position_min or self.encoder_counter > self.real_position_max:
                        self._moving_thread_target = (self.real_position_min if real_step < 0 else self.real_position_max)
                        self.encoder_counter = self._moving_thread_target
                        self.position_counter = self.encoder_counter
                        logging.debug("MGMSG_MOT_MOVE_STOPPED")
                        params = st.pack('<HihHI', self.id, self.position_counter, self.actual_velocity, 0, self.status)
                        self.parent_controller._push_return_msg_on_buffer(Message(message.MGMSG_MOT_MOVE_STOPPED, data=params))
                        if (self.status & 0x00000F00) >> 8 == 2:
                            self.status &= 0xFFFFF0FF
                            self.status |= 0x100
                        self.status &= 0xFFFFFFF0
                        self.status |= 0x1 if real_step < 0 else 0x2
                        self.current_movement_type = Channel.MovementType.No
                    elif self._moving_thread_target == self.encoder_counter:
                        if not self.parent_controller._suspend_end_of_move_messages:
                            if self.current_movement_type is not Channel.MovementType.Homing:
                                logging.debug("MGMSG_MOT_MOVE_COMPLETED")
                                params = st.pack('<HihHI', self.id, self.position_counter, self.actual_velocity, 0, self.status)
                                self.parent_controller._push_return_msg_on_buffer(Message(message.MGMSG_MOT_MOVE_COMPLETED, data=params))
                            else:
                                logging.debug("MGMSG_MOT_MOVE_HOMED")
                                self.status &= 0xFFFFF0F0
                                self.status |= 0x400
                                self.status |= 0x1 if real_step < 0 else 0x2
                                self.parent_controller._push_return_msg_on_buffer(Message(message.MGMSG_MOT_MOVE_HOMED, param1=self.id))
                else:
                    if self.current_movement_type == Channel.MovementType.Homing:
                        logging.debug("MGMSG_MOT_MOVE_HOMED")
                        self.status &= 0xFFFFF0F0
                        self.status |= 0x400
                        self.status |= 0x1 if self._moving_thread_target == self.real_position_min else 0x2
                        self.parent_controller._push_return_msg_on_buffer(Message(message.MGMSG_MOT_MOVE_HOMED, param1=self.id))
                    self.actual_velocity = 0
                    self.status &= 0xFFFFFF0F
                    self.current_movement_type = Channel.MovementType.No

    def _stop_moving_thread(self, wait_ms=1000):
        """
        Stops moving thread.
        First signals worker thread that it should finish, then waits for it for given timeout. If thread is not done
        after given timeout, an timeout exception is thrown.
        """
        if self._moving_thread is not None:
            self._moving_thread_stop_requested = True
            self._moving_thread.join(timeout=wait_ms/float(1000))
            if self._moving_thread.isAlive():
                raise TimeoutException("Attempt to close moving thread of Channel no." + str(self.id) + " timed out!")
            else:
                self._moving_thread = None

    def stop(self):
        self._stop_moving_thread()

    def __del__(self):
        self.stop()

