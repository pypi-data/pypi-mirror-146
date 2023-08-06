# -*- coding: utf-8 -*-
"""
Created on 05.05.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
try:
    import queue
except ImportError:
    import Queue as queue
import threading
import time


class CurrentStatus(object):
    """
    Class taking care of different status update message processing when automatic status updates are enabled and when
    they are not, so that outside world does not have to care about the difference
    """

    def __init__(self):
        """
        C'tor
        """
        self._mode_auto = False
        self._change_mode_lock = threading.Lock()
        self._rw_msg_lock = threading.Lock()
        self._not_empty = threading.Condition(self._rw_msg_lock)
        self._queue = queue.Queue()
        self._msg = None

    def qsize(self):
        """
        Called from main thread.
        _rw_msg_lock necessary to synchronize with put() as it is called from different thread (Message Listener worker thread)

        not synchronized with get() nor change_mode() as they are supposed to be called from the same thread (main) => calling qsize() and get() (or change_mode())
        from different threads might result in deadlock
        """
        if self._mode_auto:
            with self._rw_msg_lock:
                return 1 if self._msg else 0
        else:
            return self._queue.qsize()

    def get_mode_auto(self):
        """
        Called from main thread.
        """
        return self._mode_auto

    def change_mode(self, mode_auto):
        """
        Called from main thread.
        _change_mode_lock necessary to synchronize with put() as it is called from different thread (Message Listener worker thread)

        not synchronized with get() nor qsize() as they are supposed to be called from the same thread (main) => calling change_mode() and get() (or qsize())
        from different threads might result in deadlock
        """
        with self._change_mode_lock:
            if not mode_auto:
                self._mode_auto = False
                self._queue = queue.Queue()
            else:
                self._mode_auto = True
                self._msg = None

    def put(self, item, block=True, timeout=None):
        """
        Called from Message Listener worker thread.

        _change_mode_lock necessary to synchronize with change_mode() as it is called from different thread (main)
        _rw_msg_lock necessary to synchronize with get() and qsize() as they are called from different thread (main)
        """
        with self._change_mode_lock:
            if self._mode_auto is False:
                self._queue.put(item, block, timeout)
            else:
                """
                not necessary to take block and timeout into account here as the queue is not limited in size
                if you want to use size-limited queue don't forget to update this block of code (see Queue.put() implementation
                for inspiration)
                """
                with self._rw_msg_lock:
                    self._msg = item
                    self._not_empty.notify()

    def get(self, block=True, timeout=None):
        """
        Called from main thread.
        _not_empty (with _rw_msg_lock underneath) necessary to synchronize with put() as it is called from different thread (Message Listener worker thread)

        not synchronized with change_mode() nor qsize() as they are supposed to be called from the same thread (main) => calling get() and change_mode() (or qsize())
        from different threads might result in deadlock
        """
        if self._mode_auto is False:
            # print "CurrentStatus() taken from QUEUE"
            return self._queue.get(block, timeout)
        else:
            self._not_empty.acquire()
            try:
                if not block:
                    if self._msg is None:
                        raise queue.Empty
                elif timeout is None:
                    while self._msg is None:
                        self._not_empty.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time.time() + timeout
                    while self._msg is None:
                        remaining = endtime - time.time()
                        if remaining <= 0.0:
                            raise queue.Empty
                        self._not_empty.wait(remaining)
                item = self._msg
                # self.not_full.notify()
                # print "CurrentStatus() taken from STR"
                return item
            finally:
                self._not_empty.release()