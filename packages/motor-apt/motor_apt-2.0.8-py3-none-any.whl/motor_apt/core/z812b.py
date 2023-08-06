# -*- coding: utf-8 -*-
"""
Created by gregory on 17.07.15

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
__author__ = 'gregory'
__copyright__ = "Copyright 2015, Alpes Lasers SA"

import logging

from motor_apt.core.extended_controller import ExtendedController
from motor_apt.core.property_extensions import classproperty


class Z812B(ExtendedController):
    """
    A controller for a Z812B linear motor
    """

    @classproperty
    def max_velocity(self):
        # http://www.thorlabs.de/thorproduct.cfm?partnumber=Z812B
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 2.3 # from the manual

    @classproperty
    def max_acceleration(self):
        # http://www.thorlabs.de/thorproduct.cfm?partnumber=Z812B
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 2.3 # from nowhere

    @classproperty
    def enccnt(self):
        # from the manual
        # encoder counts per revolution of the output shaft: 512
        # gearbox ratio: 67
        # lead screw pitch is 1.0 mm
        # required return type: float
        return 34403.0

    @classproperty
    def T(self):
        # from the manual
        # required return type: float
        return 2048/6e6

    def set_device_defaults(self):
        """
        Sets some default parameters for the device, as found in the Thorlabs User Software
        """
        logging.debug("Setting device defaults")

        self.set_velocity_parameters(acceleration=1.5, max_velocity=2.0)
        logging.debug("Moves - Velocity Profile: " + str(self.velocity_parameters()))

        self.set_jog_parameters(jog_mode=2, step_size=1, acceleration=2, max_velocity=2, stop_mode=2)
        logging.debug("Jogs Settings: " + str(self.jog_parameters()))

        self.set_backlash_settings(backlash_distance=0.025)
        logging.debug("Backlash Correction: " + str(self.backlash_settings()))

        self.set_home_parameters(direction=2, limit_switch=1, velocity=1, distance_offset=0.3)
        logging.debug("Homing: " + str(self.home_parameters()))

        self.set_limit_switch_parameters(cw_hard=2, ccw_hard=2)
        logging.debug("Limit Switches: " + str(self.limit_switch_parameters()))

        self.set_dc_pid_parameters(proportional_gain=435, integral_gain=1095, differential_gain=993, integral_limit=195)
        logging.debug("Servo Loop (PID) Control settings: " + str(self.dc_pid_parameters()))

        logging.debug("Device defaults set")
