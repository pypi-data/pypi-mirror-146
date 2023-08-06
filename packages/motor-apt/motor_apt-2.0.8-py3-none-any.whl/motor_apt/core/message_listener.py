# -*- coding: utf-8 -*-
"""
Created on 04.05.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from threading import Thread
import threading
import time
import logging

from pylibftdi import FtdiError

from motor_apt.core.current_status import CurrentStatus
from motor_apt.core.pyAPT import message
from motor_apt.core.timeout_exception import TimeoutException


class MessageListener(object):
    """
    Class used to listen to messages from controller / stage.

    For storing messages a dictionary of queues is used (one queue per message type).
    """

    MESSAGES_TO_EXPECT = [message.MGMSG_HW_GET_INFO,
                          message.MGMSG_MOT_MOVE_HOMED,
                          message.MGMSG_MOT_MOVE_COMPLETED,
                          message.MGMSG_MOT_GET_HOMEPARAMS,
                          message.MGMSG_MOT_GET_POSCOUNTER,
                          message.MGMSG_MOT_GET_ENCCOUNTER,
                          message.MGMSG_MOT_GET_DCSTATUSUPDATE,
                          message.MGMSG_MOT_GET_VELPARAMS,
                          message.MGMSG_MOT_GET_JOGPARAMS,
                          message.MGMSG_MOT_GET_GENMOVEPARAMS,
                          message.MGMSG_MOT_GET_LIMSWITCHPARAMS,
                          message.MGMSG_MOT_MOVE_STOPPED,
                          message.MGMSG_MOT_GET_DCPIDPARAMS]

    NO_WAIT_MESSAGES_TO_EXPECT = [message.MGMSG_MOT_MOVE_HOMED,
                                  message.MGMSG_MOT_MOVE_COMPLETED]

    def __init__(self, controller):
        """
        C'tor
        """
        self.controller = controller
        self._thread = None
        self.message_queue = MessageListener._initialize_message_queue()
        self._stop_requested = False
        self.closing = False
        self._no_wait_message_flag = False
        self._no_wait_message_flag_lock = threading.Lock()

    @staticmethod
    def _initialize_message_queue():
        """
        Initializes the dictionary of queues.

        For processing of MGMSG_MOT_GET_DCSTATUSUPDATE message CurrentStatus class is used. To match with Queue basic
        interface, it implements put and get methods with exactly same signature as those of Queue.
        """
        ret = {}
        for messageID in MessageListener.MESSAGES_TO_EXPECT:
            ret[messageID] = Queue()
        ret[message.MGMSG_MOT_GET_DCSTATUSUPDATE] = CurrentStatus()
        return ret

    def set_no_wait_message_flag(self, value=True):
        """
        Synchronizes access to _no_wait_message_flag, which is used for throwing away messages that are not awaited,
        so that they do not pile up.
        """
        if self.controller.force_permanent_message_production:
            with self._no_wait_message_flag_lock:
                if self._no_wait_message_flag == value:
                    return
                else:
                    self._no_wait_message_flag = value
                    logging.debug("Flag " + ("" if value else "un") + "set")

    def get_no_wait_message_flag(self):
        """
        Synchronizes access to _no_wait_message_flag, which is used for throwing away messages that are not awaited,
        so that they do not pile up.
        """
        if self.controller.force_permanent_message_production:
            with self._no_wait_message_flag_lock:
                return self._no_wait_message_flag

    def start(self):
        """
        Starts the worker thread.
        """
        if self._thread is None:
            self._stop_requested = False
            self.closing = False
            self._thread = Thread(target=self._worker)
            self._thread.daemon = True
            self._thread.start()

    def _worker(self):
        """
        Worker thread - reads and processes messages from controller / stage until it is requested to stop by main thread.
        """
        while not self._stop_requested:
            # print "Message Listener: read started"
            try:
                msg = self.controller._read_message()
            except TimeoutException:
                continue
            except FtdiError as err:
                if self.closing is True:
                    logging.info("Cannot read from Ftdi as it is already closed => no more incoming messages => "
                                 "Message Listener useless => Message Listener will be terminated")
                    return
                else:
                    raise err
            # print "Message Listener: read finished"
            if msg.messageID in self.message_queue:
                with self._no_wait_message_flag_lock:
                    if msg.messageID in [message.MGMSG_MOT_MOVE_HOMED, message.MGMSG_MOT_MOVE_COMPLETED, message.MGMSG_MOT_MOVE_STOPPED] \
                            and self._no_wait_message_flag is True:
                        self._no_wait_message_flag = False
                        logging.debug("Flag unset")
                        logging.debug("Message Listener received message: " + str(msg))
                        continue
                # print "Message Listener: put started"
                self.message_queue[msg.messageID].put(msg)
                # print "Message Listener: put finished"
                logging.debug("Message Listener received message: " + str(msg))
            elif msg.messageID == message.MGMSG_HW_RESPONSE or msg.messageID == message.MGMSG_HW_RICHRESPONSE:
                logging.error("Message Listener received Error message: " + str(msg))
            else:
                logging.error("Message Listener received Unexpected message: " + str(msg))

            time.sleep(0.01)

    def stop(self, wait_ms=1000):
        """
        Stops worker thread.
        First signals worker thread that it should finish, then waits for it for given timeout. If thread is not done
        after given timeout, an timeout exception is thrown.
        """
        if self._thread is not None:
            self._stop_requested = True
            self._thread.join(timeout=wait_ms/float(1000))
            if self._thread.isAlive():
                raise TimeoutException("Attempt to close Message Listener timed out!")
            else:
                self._thread = None
