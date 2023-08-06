# -*- coding: utf-8 -*-
"""
Created by gregory on 16.10.17

Copyright 2017 Alpes Lasers SA, Neuchatel, Switzerland
"""

import logging
import threading

import time
import math
import pylibftdi

logger = logging.getLogger(__name__)

__author__ = 'gregory'
__copyright__ = "Copyright 2017, Alpes Lasers SA"


def decimal_to_hex_string(x, num_bytes):
    if x < 0:
        x += 1 << (num_bytes * 8)
    return '{0:0{1}X}'.format(x, num_bytes * 2).encode('ascii')


def hex_string_to_decimal(s, signed=True):
    num_bytes = len(s) / 2
    x = int(s, 16)
    if signed and x >= 1 << (num_bytes * 8 - 1):
        x -= 1 << (num_bytes * 8)
    return x


class ELL8(object):

    def __init__(self, serial=None, address=b'0'):
        self.serial = serial
        self.address = address
        self.units_per_rot = None
        self._device_lock = threading.RLock()
        if 0x6015 not in pylibftdi.USB_PID_LIST:
            pylibftdi.USB_PID_LIST.append(0x6015)

        self.device = pylibftdi.Device(device_id=self.serial, lazy_open=True)

    def open(self):
        with self._device_lock:
            self.device.open()
        rsp = self.query(b'in')
        # bi_positional_slider = rsp[3:5]
        self.serial = rsp[5:13]
        self.manufacturing_year = rsp[13:17]
        self.firmware_release = rsp[17] + '.' + rsp[18]
        self.hw_release = hex_string_to_decimal(rsp[19:21])
        self.thread_type = self.hw_release >> 7
        self.hw_release -= self.thread_type
        self.travel = hex_string_to_decimal(rsp[21:25])
        self.units_per_rot = hex_string_to_decimal(rsp[25:33], False)

    def close(self):
        with self._device_lock:
            self.device.close()

    def query(self, msg_bytes):
        with self._device_lock:
            self.device.write(self.address + msg_bytes)
            return self._read()

    def get_error_code(self):
        return hex_string_to_decimal(self.query(b'gs')[3:5], False)

    def get_home_offset(self):
        return self._counts_to_deg(hex_string_to_decimal(self.query(b'go')[3:11]))

    def set_home_offset(self, offset):
        return self.query(b'so' + decimal_to_hex_string(self._deg_to_counts_hex_string(offset), 4))

    def get_velocity_compensation(self):
        return hex_string_to_decimal(self.query(b'gv')[3:5])

    def set_velocity_compensation(self, vel_percentage):
        return self.query(b'sv' + decimal_to_hex_string(vel_percentage, 1))

    def get_position(self):
        return self._counts_to_deg(hex_string_to_decimal(self.query(b'gp')[3:11]))

    def move_abs(self, pos):
        pos = math.fmod(pos, 360)
        return self.query(b'ma' + decimal_to_hex_string(self._deg_to_counts_hex_string(pos), 4))

    def move_rel(self, increment):
        return self.query(b'mr' + decimal_to_hex_string(self._deg_to_counts_hex_string(increment), 4))

    def home(self):
        return self.query(b'ho0')

    def get_step_size(self):
        return self._counts_to_deg(hex_string_to_decimal(self.query(b'gj')[3:11]))

    def set_step_size(self, step_size):
        return self.query(b'sj' + decimal_to_hex_string(self._deg_to_counts_hex_string(step_size), 4))

    def step_forward(self):
        return self.query(b'fw')

    def step_backward(self):
        return self.query(b'bw')

    def restore_factory_settings(self):
        logger.info('Resetting motor 1...')
        self.query(b'f18FFF')
        self.query(b'b18FFF')
        self.query(b'us')
        time.sleep(5)
        logger.info('Resetting motor 2...')
        # TODO: not working ??
        self.query(b'f28FFF')
        self.query(b'b28FFF')
        self.query(b'us')
        time.sleep(5)

    def _read(self, timeout=10):
        with self._device_lock:
            start = time.time()
            data = ''
            while '\r\n' not in data:
                buf = self.device.read(100)
                data += buf
                if not buf and time.time() - start > timeout:
                    raise Exception('Read time out')
                time.sleep(0.01)
            return data.split('\r\n')[0]

    def _deg_to_counts_hex_string(self, x):
        return int(x * self.units_per_rot / 360)

    def _counts_to_deg(self, x):
        return float(x * 360.0 / self.units_per_rot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # first motor
    # device_id = 'DO00CSN3'
    # second motor
    device_id = 'DO000E76'
    # device_id = None
    ell8 = ELL8(device_id)
    ell8.open()
    # ell6.restore_factory_settings()
    # time.sleep(2)
    print(ell8.get_error_code())
    # time.sleep(2)
    print(ell8.get_position())
    print(ell8.set_step_size(5))
    print(ell8.get_step_size())
    print(ell8.get_home_offset())
    # print(ell6.step_forward())
    # print(ell6.move_rel(-360))

    print('Attempt homing...')
    print(ell8.home())
    print(ell8.move_abs(0))
    print(ell8.get_position())
    print(ell8.move_abs(359))
    print(ell8.get_position())
    print(ell8.move_abs(120))
    while True:
        try:
            print(ell8.get_position())
            time.sleep(0.1)
        except KeyboardInterrupt:
            print(ell8.get_error_code())