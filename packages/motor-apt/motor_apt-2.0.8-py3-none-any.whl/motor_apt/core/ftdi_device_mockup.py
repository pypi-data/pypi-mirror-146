# -*- coding: utf-8 -*-
"""
Created on 05.06.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
from abc import abstractmethod, ABCMeta

from pylibftdi import Device, FtdiError, FLUSH_BOTH, FLUSH_INPUT, FLUSH_OUTPUT


class FtdiDeviceMockup(Device, metaclass=ABCMeta):

    def __init__(self, device_id="FTDI Device Mockup", mode="b",
                 encoding="latin1", lazy_open=False):
        """
        Device([device_id[, mode, [OPTIONS ...]]) -> Device instance

        represents a single FTDI device accessible via the libftdi driver.
        Supports a basic file-like interface (open/close/read/write, context
        manager support).

        :param device_id: an optional serial number of the device to open.
            if omitted, this refers to the first device found, which is
            convenient if only one device is attached, but otherwise
            fairly useless.

        :param mode: either 'b' (binary) or 't' (text). This primarily affects
            Python 3 calls to read() and write(), which will accept/return
            unicode strings which will be encoded/decoded according to the given...

        :param encoding: the codec name to be used for text operations.

        :param lazy_open: if True, then the device will not be opened immediately -
            the user must perform an explicit open() call prior to other
            operations.

        :param chunk_size: if non-zero, split read and write operations into chunks
            of this size. With large or slow accesses, interruptions (i.e.
            KeyboardInterrupt) may not happen in a timely fashion.

        :param interface_select: select interface to use on multi-interface devices

        :param device_index: optional index of the device to open, in the
            event of multiple matches for other parameters (PID, VID,
            device_id). Defaults to zero (the first device found).
        """
        self._opened = False
        self.device_id = device_id
        # mode can be either 'b' for binary, or 't' for text.
        # if set to text, the values returned from read() will
        # be decoded using encoding before being returned as
        # strings; for binary the raw bytes will be returned.
        # This will only affect Python3.
        self.mode = mode
        # when giving a str to Device.write(), it is encoded.
        # default is latin1, because it provides
        # a one-to-one correspondence for code points 0-FF
        self.encoding = encoding
        # lazy_open tells us not to open immediately.
        if not lazy_open:
            self.open()

    def open(self):
        """
        open connection to a FTDI device
        """
        if self._opened:
            return
        self._opened = True

    def _open_device(self):
        """
        Actually open the target device

        :return: status of the open command (0 = success)
        :rtype: int
        """
        raise NotImplementedError("this method is not used in mockup")

    def close(self):
        "close our connection, free resources"
        if self._opened:
            pass
        self._opened = False

    @property
    def baudrate(self):
        """
        get or set the baudrate of the FTDI device. Re-read after setting
        to ensure baudrate was accepted by the driver.
        """
        raise NotImplementedError("this property is not used in mockup")

    @baudrate.setter
    def baudrate(self, value):
        raise NotImplementedError("this property is not used in mockup")

    def _read(self, length):
        """
        actually do the low level reading

        :return: bytes read from the device
        :rtype: bytes
        """
        raise NotImplementedError("this method is not used in mockup")

    def read(self, length):
        """
        read(length) -> bytes/string of up to `length` bytes.

        read upto `length` bytes from the FTDI device
        :param length: maximum number of bytes to read
        :return: value read from device
        :rtype: bytes if self.mode is 'b', else decode with self.encoding
        """
        if not self._opened:
            raise FtdiError("read() on closed Device")

        byte_data = self._on_read(length)

        if self.mode == 'b':
            return byte_data
        else:
            # TODO: for some codecs, this may choke if we haven't read the
            # full required data. If this is the case we should probably trim
            # a byte at a time from the output until the decoding works, and
            # buffer the remainder for next time.
            return byte_data.decode(self.encoding)

    @abstractmethod
    def _on_read(self, length):
        return some_byte_data

    def _write(self, byte_data):
        """
        actually do the low level writing

        :param byte_data: data to be written
        :type byte_data: bytes
        :return: number of bytes written
        """
        raise NotImplementedError("this method is not used in mockup")

    def write(self, data):
        """
        write(data) -> count of bytes actually written

        write given `data` string to the FTDI device

        :param data: string to be written
        :type data: string or bytes
        :return: count of bytes written, which may be less than `len(data)`
        """
        if not self._opened:
            raise FtdiError("write() on closed Device")

        try:
            byte_data = bytes(data)
        except TypeError:
            # this will happen if we are Python3 and data is a str.
            byte_data = data.encode(self.encoding)

        no_of_bytes_written = self._on_write(byte_data)

        return no_of_bytes_written

    @abstractmethod
    def _on_write(self, byte_data):
        return no_of_bytes_written

    @abstractmethod
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
        pass

    def get_error_string(self):
        """
        :return: error string from libftdi driver
        """
        raise NotImplementedError("this method is not used in mockup")
