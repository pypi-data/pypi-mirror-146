# -*- coding: utf-8 -*-
"""
Created by gregory on 18.04.16

Copyright 2016 Alpes Lasers SA, Neuchatel, Switzerland
"""

import logging
import threading
import time

import pylibftdi
from pylibftdi import FtdiError

from motor_apt.core2.message import Message
from motor_apt.core2 import message

logger = logging.getLogger(__name__)

__author__ = 'gregory'
__copyright__ = "Copyright 2016, Alpes Lasers SA"


class MessageDevice(object):
    def __init__(self, serial_number=None):
        super(MessageDevice, self).__init__()

        self._device = None
        self._message_handlers = []
        self._handler_lock = threading.Lock()
        self._write_lock = threading.RLock()
        self._message_pump_thread = None
        self._message_pump_stop = threading.Event()

        if type(serial_number) == bytes:
            self.serial_number = serial_number.decode()
        elif serial_number is not None:
            self.serial_number = str(serial_number)
        else:
            self.serial_number = None

    def __del__(self):
        self.close()

    def open(self):
        """Open the device"""
        with self._write_lock:
            if not self._device:
                # this takes up to 2-3s:
                dev = pylibftdi.Device(mode='b', device_id=self.serial_number)
                dev.baudrate = 115200

                def _checked_c(ret):
                    if not ret == 0:
                        raise Exception(dev.ftdi_fn.ftdi_get_error_string())

                _checked_c(dev.ftdi_fn.ftdi_set_line_property(8,  # number of bits
                                                              1,  # number of stop bits
                                                              0  # no parity
                                                              ))
                time.sleep(50.0 / 1000)

                dev.flush(pylibftdi.FLUSH_BOTH)

                time.sleep(50.0 / 1000)

                # skipping reset part since it looks like pylibftdi does it already

                # this is pulled from ftdi.h
                _checked_c(dev.ftdi_fn.ftdi_setflowctrl(0x1 << 8))
                _checked_c(dev.ftdi_fn.ftdi_setrts(1))

                self._device = dev

                # Start the message pump
                self._message_pump_stop.clear()
                self._message_pump_thread = threading.Thread(target=self._message_pump)
                self._message_pump_thread.start()

    def close(self):
        """Close the device"""
        with self._write_lock:
            if self._device and not self._device.closed:
                # Stop the message pump
                self._message_pump_stop.set()
                if self._message_pump_thread and self._message_pump_thread.is_alive():
                    self._message_pump_thread.join(6)

                # Actually close the device
                self._device.close()
                self._device = None

    def query(self, m, expected_message_id, timeout=300):
        """Sends the message m, waits for a response message of the given id and returns it. Returns None if the
        expected message was not read before the timeout. Thread safe."""

        # Signals that the expected message arrived
        finished = threading.Event()

        # Used to store the message in the closure.
        ret_mesg = {}

        # Message handler that receives the messages of the device through the message pump
        def handler(msg):
            # msg=None means that the message pump failed and we must stop there
            if msg is None or msg.messageID == expected_message_id:
                finished.set()
                ret_mesg['msg'] = msg

        # Add the handler safely
        with self._handler_lock:
            self._message_handlers.append(handler)

        self.send_message(m)

        # When the correct message arrives, it is handled by the handler and finished is set
        # finished is also set if the message pump fails.
        finished.wait(timeout)

        # Remove the handler safely
        with self._handler_lock:
            self._message_handlers.remove(handler)

        # Return the expected message or None
        return ret_mesg.get('msg')

    def send_message(self, m):
        """Send a message to the device. Thread safe (there is a lock that prevents concurrent write)"""
        with self._write_lock:
            self._device.write(m.pack())

    def _pump_loop_hook(self):
        """This is called on each loop of the message pump. Can be implemented by subclasses to do something on each
        iteration (e.g. server keepalive)"""
        pass

    def _message_pump(self):
        """Loop that reads the messages transmitted by the device. Sends the read messages to the message handlers that
        are currently registered. If a read fails, it tries to reboot the device automatically (NB if the reboot fails,
        it stops -- not an endless loop)."""
        try:
            try:
                while not self._message_pump_stop.is_set():
                    msg = self._read_message(0.5)
                    if msg:
                        with self._handler_lock:
                            for mh in self._message_handlers:
                                mh(msg)
                    time.sleep(0.05)
            finally:
                # close the handlers upon exiting the message pump.
                with self._handler_lock:
                    for mh in self._message_handlers:
                        mh(None)
                self._message_handlers = []

        except FtdiError:
            logging.debug('Error in message pump, trying to recover.', exc_info=1)

            # Try to restart in a new thread (the close method joins the current thread)
            time.sleep(1)

            def reopen():
                self.close()
                self.open()

            threading.Thread(target=reopen).start()

    def _read(self, length, timeout=5.0):
        """ Returns empty bytes if no data is obtained before the timeout, raises an exception if some data shorter than
        length is obtained and then no further data arrives before the timeout expires
        """
        data = bytes()
        end = time.time() + timeout
        while len(data) < length and time.time() < end:
            diff = length - len(data)
            read = self._device.read(diff)
            if read:
                end = time.time() + timeout
                data += read
                if length - len(data) == 0:
                    return data
            time.sleep(0.05)

        if len(data) > 0:
            raise RuntimeError('Read on {} timed out'.format(str(self)))

        return data

    def _read_message(self, timeout=5.0):
        """Tries to read a single message from the device. Returns None if no message gets there before the timeout."""
        data = self._read(message.MGMSG_HEADER_SIZE, timeout)
        if data:
            msg = Message.unpack(data, header_only=True)
            if msg.hasdata:
                data = self._read(msg.datalength)
                msglist = list(msg)
                msglist[-1] = data
                return Message._make(msglist)
            return msg
        return None

    def __str__(self):
        return 'MessageDevice(serial=%s, device=%s)' % (self.serial_number, self._device)