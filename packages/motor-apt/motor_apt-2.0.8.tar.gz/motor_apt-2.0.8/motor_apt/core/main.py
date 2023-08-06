# -*- coding: utf-8 -*-
"""
Application for controlling motors from Thorlabs

Created on April 17, 2015

Copyright Alpes Lasers SA, Neuchatel, Switzerland, 2015

@author: juraj
"""
import time
# import logging
# import sys

from motor_apt.utils.parser import parser
import pylibftdi

from motor_apt.core.cr1 import CR1
from motor_apt.core.cr1_mockup import CR1Mockup


class Core(object):
    """
    Base class
    """
    def __init__(self):
        """
        C'tor
        """
        # self.log = logging.getLogger(self.__class__.__name__)
        # self.log.addHander(logging.StreamHandler())

    def run(self):
        """
        This method is called at run time.
        """
        # rmmod ftdi_sio
        # rmmod usbserial
        # self.log.info("Logging something")
        serial = "83851458"

        try:
            with CR1(serial_number=serial, force_permanent_message_production=True, mockup=CR1Mockup()) as con:

                print("Identify requested")
                con.identify()

                print("Start update messages requested")
                con.start_update_messages()
                print("Sleep 5 seconds started")
                time.sleep(5)
                print("Sleep 5 seconds finished")
                print("Stop update messages requested")
                con.stop_update_messages()
                print("Sleep 5 seconds started")
                time.sleep(5)
                print("Sleep 5 seconds finished")

                print("HW Info: " + str(con.info()))

                con.set_position_counter(position=2.5)
                print("Position: " + str(con.position_counter()))

                con.set_encoder_counter(enc_count=4096)
                print("Encoder count: " + str(con.encoder_counter()))

                con.set_velocity_parameters(acceleration=4.00024, max_velocity=4.00024)
                print("Moves - Velocity Profile: " + str(con.velocity_parameters()))

                con.set_jog_parameters(jog_mode=2, step_size=0.999756, acceleration=2.99988, max_velocity=2.99988, stop_mode=2)
                print("Jogs Settings: " + str(con.jog_parameters()))

                con.set_backlash_settings(backlash_distance=0.2001954)
                print("Backlash Correction: " + str(con.backlash_settings()))

                # con.set_home_parameters(direction=2, limit_switch=1, velocity=2.00012, distance_offset=0.200195)
                # print "Homing: " + str(con.home_parameters())

                con.set_limit_switch_parameters(cw_hard=1, ccw_hard=1)
                print("Limit Switches: " + str(con.limit_switch_parameters()))

                con.set_dc_pid_parameters(proportional_gain=850, integral_gain=50, differential_gain=2720, integral_limit=50)
                print("Servo Loop (PID) Control settings: " + str(con.dc_pid_parameters()))

                print("\nRelative move by 10° started")
                con.move_relative(rel_pos_mm=10, wait=True)
                print("Relative move by 10° finished")

                print("\nAbsolute move to position 10° started")
                con.move_absolute(abs_pos_mm=10, wait=False)
                print("Absolute move to position 10° finished")

                time.sleep(10)

                print("\nContinuous move in backward direction started")
                con.move_continuous(direction=2)
                print("Sleep 5 seconds started")
                time.sleep(5)
                print("Sleep 5 seconds finished")
                print("Stop requested")
                con.stop(wait=True)
                print("Stopped")

                print("Jog started")
                con.jog(wait=True)
                print("Jog finished")

                # print "\nHoming started"
                # con.home()
                # print "Homing finished"

                print("\nStatus: " + str(con.status()))

                print("\nDisconnect requested")
                con.disconnect()
                print("Disconnect finished")

                return 0
        except pylibftdi.FtdiError:
            print('\tCould not find APT controller S/N of', serial)
            return 1


def main():
    # parser.add_argument("-X", "--X", help="Some option", dest="somevar")
    # options = parser.parse_args()
    # Do something with the options, like pass them to the class below
    app = Core()
    app.run()

if __name__ == "__main__":
    main()