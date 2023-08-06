# -*- coding: utf-8 -*- 
"""
Created on April 17, 2015

Copyright Alpes Lasers SA, Neuchatel, Switzerland, 2015

@author: juraj
"""

import unittest
import time


serial = "83851458"
enc_res_in_deg = 0.0006103515625
vel_res_in_deg_over_s = 0.0000272848410532
acc_res_in_deg_over_s2 = 0.07993605777301127
pos_err_in_enccounts = 6  # allowed position error in enccounts


class TestMain(unittest.TestCase):

    def test_import(self):
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

    def setUp(self):
        """
        It is necessary to put device into defined state before each test, so that the tests do not affect each other.
        """
        self.set_device_defaults()

    def set_device_defaults(self):
        """
        Sets devices into defined state.
        """
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:

            print("Setting device defaults")

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

            con.set_encoder_counter(0)
            print("Encoder counter: " + str(con.encoder_counter()))

            print("Device defaults set")

    def assertQueuesEmpty(self, controller):
        for key in controller.message_listener.message_queue.keys():
            qsize = controller.message_listener.message_queue[key].qsize()
            if qsize != 0:
                raise AssertionError("Message queue for message " + "0x{0:04X}".format(key) + " is not empty! "
                                     "No. of unprocessed messages: " + str(qsize))
        if controller.message_listener.get_no_wait_message_flag():
            raise AssertionError("no_wait_message flag is not supposed to be set!")

    def test_cr1_custom_1(self):
        print("[test_cr1_custom_1]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:

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

            # print("\nHoming started")
            # con.home()
            # print("Homing finished")

            print("\nStatus: " + str(con.status()))

            print("\nDisconnect requested")
            con.disconnect()

            self.assertQueuesEmpty(con)

    def test_cr1_custom_2(self):
        print("[test_cr1_custom_2]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_continuous(direction=2)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_continuous(direction=2)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_continuous(direction=2)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_continuous(direction=2)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

    def test_cr1_custom_3(self):
        print("[test_cr1_custom_3]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_relative(rel_pos_mm=15, wait=True)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_relative(rel_pos_mm=15, wait=False)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_relative(rel_pos_mm=15, wait=False)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            con.move_relative(rel_pos_mm=15, wait=True)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_relative(rel_pos_mm=15, wait=False)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_relative(rel_pos_mm=15, wait=True)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_relative(rel_pos_mm=15, wait=True)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            con.move_relative(rel_pos_mm=15, wait=False)
            time.sleep(2.5)
            con.stop(wait=False)
            con.stop(wait=True)
            con.stop(wait=False)

            self.assertQueuesEmpty(con)

    def test_cr1_custom_4(self):
        print("[test_cr1_custom_4]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            print("Start update messages requested")
            con.start_update_messages()

            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)

            print("\nSleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")

            print("\nRelative move by 5° started")
            con.move_relative(rel_pos_mm=5, wait=True)
            print("Relative move by 5° finished")

            print("\nSleep 10 seconds started")
            time.sleep(10)
            print("Sleep 10 seconds finished")

            print("Stop update messages requested")
            con.stop_update_messages()

            print("\nStatus: " + str(con.status()))

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            print("Start update messages requested")
            con.start_update_messages()

            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)

            print("\nSleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")

            print("\nRelative move by 5° started")
            con.move_relative(rel_pos_mm=5, wait=True)
            print("Relative move by 5° finished")

            print("\nSleep 10 seconds started")
            time.sleep(10)
            print("Sleep 10 seconds finished")

            print("Stop update messages requested")
            con.stop_update_messages()

            print("\nStatus: " + str(con.status()))

            self.assertQueuesEmpty(con)

    def test_cr1_custom_5(self):
        print("[test_cr1_custom_5]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:

            print("\nRelative move by -15° started")
            con.move_relative(rel_pos_mm=-15, wait=False)
            print("Relative move by -15° finished")

            time.sleep(2)

            print("\nAbsolute move to position 10° started")
            con.move_absolute(abs_pos_mm=10, wait=True)
            print("Absolute move to position 10° finished")

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:

            print("\nRelative move by -15° started")
            con.move_relative(rel_pos_mm=-15, wait=False)
            print("Relative move by -15° finished")

            time.sleep(2)

            print("\nAbsolute move to position 10° started")
            con.move_absolute(abs_pos_mm=10, wait=True)
            print("Absolute move to position 10° finished")

            self.assertQueuesEmpty(con)

    def test_cr1_custom_6(self):
        print("[test_cr1_custom_6]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:

            print("\nRelative move by -15° started")
            con.move_relative(rel_pos_mm=-15, wait=False)
            print("Relative move by -15° finished")

            time.sleep(2)

            print("\nAbsolute move to position 10° started")
            con.move_absolute(abs_pos_mm=10, wait=False)
            print("Absolute move to position 10° finished")

            time.sleep(10)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:

            print("\nRelative move by -15° started")
            con.move_relative(rel_pos_mm=-15, wait=False)
            print("Relative move by -15° finished")

            time.sleep(2)

            print("\nAbsolute move to position 10° started")
            con.move_absolute(abs_pos_mm=10, wait=False)
            print("Absolute move to position 10° finished")

            time.sleep(10)

            self.assertQueuesEmpty(con)

    def test_cr1_start_stop_update_messages_and_status(self):
        print("[test_cr1_start_stop_update_messages_and_status]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            print("Start update messages requested")
            con.start_update_messages()
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("\nStatus: " + str(con.status()))
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("Stop update messages requested")
            con.stop_update_messages()
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("\nStatus: " + str(con.status()))
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            print("Start update messages requested")
            con.start_update_messages()
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("\nStatus: " + str(con.status()))
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("Stop update messages requested")
            con.stop_update_messages()
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")
            print("\nStatus: " + str(con.status()))
            print("Sleep 2.5 seconds started")
            time.sleep(2.5)
            print("Sleep 2.5 seconds finished")

            self.assertQueuesEmpty(con)

    def test_cr1_set_velocity_parameters(self):
        print("[test_cr1_set_velocity_parameters]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            acceleration = 3.00024
            max_velocity = 3.00024
            con.set_velocity_parameters(acceleration=acceleration, max_velocity=max_velocity)
            min_vel, acc, max_vel = con.velocity_parameters()
            print("Moves - Velocity Profile: " + str((min_vel, acc, max_vel)))
            self.assertTrue(abs(acc - acceleration) <= acc_res_in_deg_over_s2 / 2)
            self.assertTrue(abs(max_vel - max_velocity) <= vel_res_in_deg_over_s / 2)

            self.assertRaises(ValueError, con.set_velocity_parameters, acceleration=-1, max_velocity=max_velocity)
            self.assertRaises(ValueError, con.set_velocity_parameters, acceleration=10, max_velocity=max_velocity)
            self.assertRaises(ValueError, con.set_velocity_parameters, acceleration=acceleration, max_velocity=-1)
            self.assertRaises(ValueError, con.set_velocity_parameters, acceleration=acceleration, max_velocity=10)

    def test_cr1_set_jog_parameters(self):
        print("[test_cr1_set_jog_parameters]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            jog_mode = 1
            step_size = 1.999756
            acceleration = 1.99888
            max_velocity = 1.99988
            stop_mode = 1
            con.set_jog_parameters(jog_mode=jog_mode, step_size=step_size,
                                   acceleration=acceleration, max_velocity=max_velocity, stop_mode=stop_mode)
            jog_mode_new, step_size_new, min_vel_new, acc_new, max_vel_new, stop_mode_new = con.jog_parameters()
            print("Jogs Settings: " + str((jog_mode_new, step_size_new, min_vel_new, acc_new, max_vel_new, stop_mode_new)))
            self.assertEqual(jog_mode, jog_mode_new)
            self.assertTrue(abs(step_size_new - step_size) <= enc_res_in_deg / 2)
            self.assertTrue(abs(acc_new - acceleration) <= acc_res_in_deg_over_s2 / 2)
            self.assertTrue(abs(max_vel_new - max_velocity) <= vel_res_in_deg_over_s / 2)
            self.assertEqual(stop_mode, stop_mode_new)

            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=0, step_size=step_size,
                              acceleration=acceleration, max_velocity=max_velocity, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=3, step_size=step_size,
                              acceleration=acceleration, max_velocity=max_velocity, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=-1,
                              acceleration=acceleration, max_velocity=max_velocity, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=-1, max_velocity=max_velocity, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=10, max_velocity=max_velocity, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=acceleration, max_velocity=-1, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=acceleration, max_velocity=10, stop_mode=stop_mode)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=acceleration, max_velocity=max_velocity, stop_mode=0)
            self.assertRaises(ValueError, con.set_jog_parameters, jog_mode=jog_mode, step_size=step_size,
                              acceleration=acceleration, max_velocity=max_velocity, stop_mode=3)

    def test_cr1_set_backlash_settings(self):
        print("[test_cr1_set_backlash_settings]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            backlash_distance = 0.1
            con.set_backlash_settings(backlash_distance=backlash_distance)
            backlash_distance_new = con.backlash_settings()
            print("Backlash Correction: " + str(backlash_distance_new))
            self.assertTrue(abs(backlash_distance_new - backlash_distance) <= enc_res_in_deg / 2)

            self.assertRaises(ValueError, con.set_backlash_settings, backlash_distance=-1)

    # def test_cr1_set_home_parameters(self):
    #     from motor_apt.core.cr1 import CR1
    #
    #     with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
    #             direction=1
    #             limit_switch=4
    #             velocity=1.00012
    #             distance_offset=0.400195
    #             con.set_home_parameters(direction=direction, limit_switch=limit_switch, velocity=velocity, distance_offset=distance_offset)
    #             direction_new, limit_switch_new, velocity_new, distance_offset_new = con.home_parameters()
    #             print("Homing: " + str((direction_new, limit_switch_new, velocity_new, distance_offset_new)))
    #             self.assertEqual(direction_new, direction)
    #             self.assertEqual(limit_switch_new, limit_switch)
    #             self.assertTrue(abs(velocity_new - velocity) < 0.004)
    #             self.assertTrue(abs(distance_offset_new - distance_offset) < 0.001)
    #
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=0, limit_switch=limit_switch, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=3, limit_switch=limit_switch, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=0, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=2, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=3, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=5, velocity=velocity, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=limit_switch, velocity=-1, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=limit_switch, velocity=10, distance_offset=distance_offset)
    #             self.assertRaises(ValueError, con.set_home_parameters, direction=direction, limit_switch=limit_switch, velocity=velocity, distance_offset=-1)

    def test_cr1_set_dc_pid_parameters(self):
        print("[test_cr1_set_dc_pid_parameters]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            proportional_gain = 850
            integral_gain = 50
            differential_gain = 2720
            integral_limit = 50
            filter_control = 0x0F
            con.set_dc_pid_parameters(proportional_gain=proportional_gain,
                                      integral_gain=integral_gain, differential_gain=differential_gain,
                                      integral_limit=integral_limit, filter_control=filter_control)
            proportional_gain_new, integral_gain_new, differential_gain_new, integral_limit_new, filter_control_new = con.dc_pid_parameters()
            print("Servo Loop (PID) Control settings: " + \
                  str((proportional_gain_new, integral_gain_new, differential_gain_new, integral_limit_new, filter_control_new)))
            self.assertEqual(proportional_gain_new, proportional_gain)
            self.assertEqual(integral_gain_new, integral_gain)
            self.assertEqual(differential_gain_new, differential_gain)
            self.assertEqual(integral_limit_new, integral_limit)
            self.assertEqual(filter_control_new, filter_control)

            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=-1,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=5.5,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=40000,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=-1, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=5.5, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=40000, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=-1,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=5.5,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=40000,
                              integral_limit=integral_limit, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=-1, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=5.5, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=40000, filter_control=filter_control)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=-1)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=5.5)
            self.assertRaises(ValueError, con.set_dc_pid_parameters, proportional_gain=proportional_gain,
                              integral_gain=integral_gain, differential_gain=differential_gain,
                              integral_limit=integral_limit, filter_control=1000)

    def test_cr1_set_limit_switch_parameters(self):
        print("[test_cr1_set_limit_switch_parameters]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            cw_hard = 2
            ccw_hard = 5
            cw_soft = 3.98494
            ccw_soft = 2.4894
            soft_mode = 1
            con.set_limit_switch_parameters(cw_hard=cw_hard, ccw_hard=ccw_hard,
                                            cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            cw_hard_new, ccw_hard_new, cw_soft_new, ccw_soft_new, soft_mode_new = con.limit_switch_parameters()
            print("Limit Switches: " + str((cw_hard_new, ccw_hard_new, cw_soft_new, ccw_soft_new, soft_mode_new)))
            self.assertEqual(cw_hard_new, cw_hard)
            self.assertEqual(ccw_hard_new, ccw_hard)
            self.assertTrue(abs(cw_soft_new - cw_soft) <= enc_res_in_deg / 2)
            self.assertTrue(abs(ccw_soft_new - ccw_soft) <= enc_res_in_deg / 2)
            self.assertEqual(soft_mode_new, soft_mode)

            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=0, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=6, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=0x81, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=0x85, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=0,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=6,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=0x81,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=0x85,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=-1, ccw_soft=ccw_soft, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=-1, soft_mode=soft_mode)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=0)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=4)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=0x80)
            self.assertRaises(ValueError, con.set_limit_switch_parameters, cw_hard=cw_hard, ccw_hard=ccw_hard,
                              cw_soft=cw_soft, ccw_soft=ccw_soft, soft_mode=0x84)

    def test_cr1_move_relative(self):
        print("[test_cr1_move_relative]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            cur_pos = con.position_counter()
            rel_mov_deg = 6.103515625
            con.move_relative(rel_mov_deg, wait=True)
            new_pos = con.position_counter()
            print(str(cur_pos) + " + " + str(rel_mov_deg) + " - " + str(new_pos) + " = " + str(cur_pos + rel_mov_deg - new_pos))
            self.assertTrue(abs(cur_pos + rel_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            rel_mov_deg2 = -6.103515625
            con.move_relative(rel_mov_deg2, wait=True)
            new_pos2 = con.position_counter()
            print(str(cur_pos2) + " + " + str(rel_mov_deg2) + " - " + str(new_pos2) + " = " + str(cur_pos2 + rel_mov_deg2 - new_pos2))
            self.assertTrue(abs(cur_pos2 + rel_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            cur_pos = con.position_counter()
            rel_mov_deg = 6.103515625
            con.move_relative(rel_mov_deg, wait=False)
            time.sleep(5)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos + rel_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            rel_mov_deg2 = -6.103515625
            con.move_relative(rel_mov_deg2, wait=False)
            time.sleep(5)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + rel_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            cur_pos = con.position_counter()
            rel_mov_deg = 6.103515625
            con.move_relative(rel_mov_deg, wait=True)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos + rel_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            rel_mov_deg2 = -6.103515625
            con.move_relative(rel_mov_deg2, wait=True)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + rel_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            cur_pos = con.position_counter()
            rel_mov_deg = 6.103515625
            con.move_relative(rel_mov_deg, wait=False)
            time.sleep(5)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos + rel_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            rel_mov_deg2 = -6.103515625
            con.move_relative(rel_mov_deg2, wait=False)
            time.sleep(5)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + rel_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

    def test_cr1_move_absolute(self):
        print("[test_cr1_move_absolute]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            abs_mov_deg = 6.103515625
            con.move_absolute(abs_mov_deg, wait=True)
            new_pos = con.position_counter()
            self.assertTrue(abs(abs_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            abs_mov_deg2 = -6.103515625
            con.move_absolute(abs_mov_deg2, wait=True)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(abs_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            abs_mov_deg = 6.103515625
            con.move_absolute(abs_mov_deg, wait=False)
            time.sleep(5)
            new_pos = con.position_counter()
            self.assertTrue(abs(abs_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            abs_mov_deg2 = -6.103515625
            con.move_absolute(abs_mov_deg2, wait=False)
            time.sleep(5)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(abs_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            abs_mov_deg = 6.103515625
            con.move_absolute(abs_mov_deg, wait=True)
            new_pos = con.position_counter()
            self.assertTrue(abs(abs_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            abs_mov_deg2 = -6.103515625
            con.move_absolute(abs_mov_deg2, wait=True)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(abs_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            abs_mov_deg = 6.103515625
            con.move_absolute(abs_mov_deg, wait=False)
            time.sleep(5)
            new_pos = con.position_counter()
            self.assertTrue(abs(abs_mov_deg - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            abs_mov_deg2 = -6.103515625
            con.move_absolute(abs_mov_deg2, wait=False)
            time.sleep(5)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(abs_mov_deg2 - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

    def test_cr1_move_continuous(self):
        print("[test_cr1_move_continuous]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            con.move_continuous(direction=2)
            time.sleep(3)
            con.stop(wait=True)

            con.move_continuous(direction=1)
            time.sleep(3)
            con.stop(wait=True)

            self.assertRaises(ValueError, con.move_continuous, direction=0)
            self.assertRaises(ValueError, con.move_continuous, direction=3)

            self.assertQueuesEmpty(con)

    def test_cr1_jog(self):
        print("[test_cr1_jog]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            jog_mode, step_size, min_vel, acc, max_vel, stop_mode = con.jog_parameters()

            self.assertRaises(ValueError, con.jog, direction=0)
            self.assertRaises(ValueError, con.jog, direction=3)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            cur_pos = con.position_counter()
            con.jog(direction=1, wait=True)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos - step_size - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            con.jog(direction=2, wait=True)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + step_size - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            cur_pos = con.position_counter()
            con.jog(direction=1, wait=False)
            time.sleep(2)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos - step_size - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            con.jog(direction=2, wait=False)
            time.sleep(2)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + step_size - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            cur_pos = con.position_counter()
            con.jog(direction=1, wait=True)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos - step_size - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            con.jog(direction=2, wait=True)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + step_size - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            cur_pos = con.position_counter()
            con.jog(direction=1, wait=False)
            time.sleep(2)
            new_pos = con.position_counter()
            self.assertTrue(abs(cur_pos - step_size - new_pos) <= enc_res_in_deg * pos_err_in_enccounts)

            cur_pos2 = con.position_counter()
            con.jog(direction=2, wait=False)
            time.sleep(2)
            new_pos2 = con.position_counter()
            self.assertTrue(abs(cur_pos2 + step_size - new_pos2) <= enc_res_in_deg * pos_err_in_enccounts)

            self.assertTrue(abs(new_pos2 - cur_pos) <= 2 * enc_res_in_deg * pos_err_in_enccounts)

            self.assertQueuesEmpty(con)

    def test_cr1_stop(self):
        print("[test_cr1_stop]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)
            print("Sleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")
            print("Stop requested")
            con.stop(wait=True)
            print("Stopped")

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=True) as con:
            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)
            print("Sleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")
            print("Stop requested")
            con.stop(wait=False)
            print("Stopped")

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)
            print("Sleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")
            print("Stop requested")
            con.stop(wait=True)
            print("Stopped")

            self.assertQueuesEmpty(con)

        with CR1(mockup=CR1Mockup(), serial_number=serial, force_permanent_message_production=False) as con:
            print("\nContinuous move in backward direction started")
            con.move_continuous(direction=2)
            print("Sleep 3 seconds started")
            time.sleep(3)
            print("Sleep 3 seconds finished")
            print("Stop requested")
            con.stop(wait=False)
            print("Stopped")

            self.assertQueuesEmpty(con)

    def test_cr1_position_counter(self):
        print("[test_cr1_position_counter]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            cur_pos_cnt = con.position_counter()
            con.set_position_counter(cur_pos_cnt + 165.8)
            new_pos_cnt = con.position_counter()
            self.assertTrue(abs(new_pos_cnt - (cur_pos_cnt + 165.8)) <= enc_res_in_deg / 2)

            cur_pos_cnt2 = con.position_counter()
            con.set_position_counter(cur_pos_cnt2 - 25.3)
            new_pos_cnt2 = con.position_counter()
            self.assertTrue(abs(new_pos_cnt2 - (cur_pos_cnt2 - 25.3)) <= enc_res_in_deg / 2)

    def test_cr1_encoder_counter(self):
        print("[test_cr1_encoder_counter]")
        from motor_apt.core.cr1 import CR1
        from motor_apt.core.cr1_mockup import CR1Mockup

        with CR1(mockup=CR1Mockup(), serial_number=serial) as con:
            cur_enc_cnt = con.encoder_counter()
            con.set_encoder_counter(cur_enc_cnt + 165)
            new_enc_cnt = con.encoder_counter()
            self.assertEqual(cur_enc_cnt + 165, new_enc_cnt)

            cur_enc_cnt2 = con.encoder_counter()
            con.set_encoder_counter(cur_enc_cnt2 - 25)
            new_enc_cnt2 = con.encoder_counter()
            self.assertEqual(cur_enc_cnt2 - 25, new_enc_cnt2)

            self.assertRaises(ValueError, con.set_encoder_counter, 4.5)