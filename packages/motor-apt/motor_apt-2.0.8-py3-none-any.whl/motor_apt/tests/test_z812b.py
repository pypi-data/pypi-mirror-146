# -*- coding: utf-8 -*-
"""
Created by gregory on 17.07.15

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
__author__ = 'gregory'
__copyright__ = "Copyright 2015, Alpes Lasers SA"


import unittest
import time

from motor_apt.core.z812b import Z812B

serial = "83858574"

class TestMain(unittest.TestCase):


    def setUp(self):
        """
        It is necessary to put device into defined state before each test, so that the tests do not affect each other.
        """
        print('set up')

    def test_connection(self):
        with Z812B(serial_number=serial) as controller:
            controller.identify()


    def assertQueuesEmpty(self, controller):
        for key in controller.message_listener.message_queue.keys():
            qsize = controller.message_listener.message_queue[key].qsize()
            if qsize != 0:
                raise AssertionError("Message queue for message " + "0x{0:04X}".format(key) + " is not empty! "
                                     "No. of unprocessed messages: " + str(qsize))
        if controller.message_listener.get_no_wait_message_flag():
            raise AssertionError("no_wait_message flag is not supposed to be set!")

    def tes2t_cr1_custom_1(self):
        print("[test_cr1_custom_1]")
        from motor_apt.core.cr1 import CR1

        with Z812B(serial_number=serial, force_permanent_message_production=True) as con:

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

            con.set_velocity_parameters(acceleration=1, max_velocity=1)
            print("Moves - Velocity Profile: " + str(con.velocity_parameters()))

            con.set_jog_parameters(jog_mode=2, step_size=0.999756, acceleration=1, max_velocity=1, stop_mode=2)
            print("Jogs Settings: " + str(con.jog_parameters()))

            con.set_backlash_settings(backlash_distance=0.2001954)
            print("Backlash Correction: " + str(con.backlash_settings()))

            con.set_home_parameters(direction=1, limit_switch=4, velocity=0.9961484514814204, distance_offset=0)
            print("Homing: " + str(con.home_parameters()))

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

            print("\nHoming started")
            con.home()
            print("Homing finished")

            print("\nStatus: " + str(con.status()))

            print("\nDisconnect requested")
            con.disconnect()

            self.assertQueuesEmpty(con)

    def test_z812b_homing(self):
        print("[test_z812b_homing]")

        with Z812B(serial_number=serial, force_permanent_message_production=True) as con:
            con.set_home_parameters(direction=1, limit_switch=4, velocity=0.9961484514814204, distance_offset=0)
            print("Homing: " + str(con.home_parameters()))

            print("\nHoming started")
            con.home(wait=True)
            print("Homing finished")

            con.set_encoder_counter(80000)
            print("Position:" + str(con.position_counter()))
            print("Enccnt:" + str(con.encoder_counter()))

            time.sleep(0.1)

            con.set_home_parameters(direction=2, limit_switch=1, velocity=0.9961484514814204, distance_offset=0)
            print("Homing: " + str(con.home_parameters()))

            print("\nHoming started")
            con.home(wait=True)
            print("Homing finished")

            print("Position:" + str(con.position_counter()))
            print("Enccnt:" + str(con.encoder_counter()))
