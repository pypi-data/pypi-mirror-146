# -*- coding: utf-8 -*-
"""
Created on 08.06.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
import struct as st
import logging
from motor_apt.core.cr1 import CR1

from motor_apt.core.pyAPT.message import Message, Messages
from motor_apt.core.thorlabs_stage_device_mockup import ThorlabsStageDeviceMockup, Channel


class CR1Mockup(ThorlabsStageDeviceMockup):
    def __init__(self):
        super(CR1Mockup, self).__init__(channels_list=[
            Channel(id=1, controller=self, position_scale=CR1.position_scale, acceleration_scale=CR1.acceleration_scale, velocity_scale=CR1.velocity_scale,
                    maximum_acceleration=CR1.max_acceleration, maximum_velocity=CR1.max_velocity,
                    switch_cw_hard=1, switch_ccw_hard=1)
        ])

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
        with self._channels[ch]._moving_lock:
            self._channels[ch].encoder_counter = position
            self._channels[ch]._moving_thread_target = position

    def _MGMSG_MOT_REQ_POSCOUNTER_handler(self, param1=0, param2=0, datastring=None):
        """
        <: small endian
        H: 2 bytes for channel
        i: 4 bytes for position
        """
        logging.debug("MGMSG_MOT_REQ_POSCOUNTER")
        if param1 not in self._channels:
            return
        with self._channels[param1]._moving_lock:
            params = st.pack('<Hi', param1, self._channels[param1].encoder_counter)
            return Message(Messages.MGMSG_MOT_GET_POSCOUNTER, data=params)