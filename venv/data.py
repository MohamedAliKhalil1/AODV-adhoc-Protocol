import threading
import time
import json

import data
from message import Message
import controller

class DataManager (threading.Thread):

    table = {}
    pendingRREP = {}
    def __init__(self, response, lock, serialport):
        threading.Thread.__init__(self)
        self.response = response
        self.threadLock = lock
        self.ser = serialport

    def run(self):
        self.threadLock.acquire()
        controller.Controller.parseRecieved(self, response)
        self.threadLock.release()


        str(data)
        data += "\r\n"
        self.ser.write(data.encode())
        sleep(1)

