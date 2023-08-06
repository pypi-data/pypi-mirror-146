# -*- coding: utf-8 -*-
"""
Created on 23.07.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
from motor_apt.core.z812b import Z812B
from motor_apt.core.thorlabs_stage_device_mockup import ThorlabsStageDeviceMockup, Channel


class Z812BMockup(ThorlabsStageDeviceMockup):
    def __init__(self):
        super(Z812BMockup, self).__init__(channels_list=[
            Channel(id=1, controller=self, position_scale=Z812B.position_scale, acceleration_scale=Z812B.acceleration_scale, velocity_scale=Z812B.velocity_scale,
                    maximum_acceleration=Z812B.max_acceleration, maximum_velocity=Z812B.max_velocity,
                    real_position_min=0, real_position_max=12,
                    switch_cw_hard=2, switch_ccw_hard=2)
        ])
