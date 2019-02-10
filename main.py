# pylint: disable=import-error

import machine
import math
import network
import os
import time
import utime
import gc
from machine import RTC
from L76GNSS import L76GNSS
from pytrack import Pytrack

# Unfortunately, the abstract base class (abc) module is not available in MicroPython
class CommunicationInterface():
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def send(self, data):
        pass


class WiFiCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up WiFi...")
        print("WiFi set up")

    def send(self, data):
        print("Sending: " + str(data))


class SigFoxCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up SigFox...")
        print("SigFox set up")

    def send(self, data):
        print("Sending: " + str(data))


class CellularCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up Cellular...")
        print("Cellular set up...")

    def send(self, data):
        print("Sending: " + str(data))


class ConsoleCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up console...")
        print("Console set up...")

    def send(self, data):
        print("Sending: " + str(data))
        print("{}".format(data))


# Unfortunately, the abstract base class (abc) module is not available in MicroPython
class GNSSInterface():
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def getLocation(self):
        pass


class PycomGNSS(GNSSInterface):
    def setup(self):
        time.sleep(2)
        gc.enable()

        # setup rtc
        rtc = machine.RTC()
        rtc.ntp_sync("pool.ntp.org")
        utime.sleep_ms(750)
        utime.timezone(7200)

        py = Pytrack()
        self.gnss = L76GNSS(py, timeout=30)

        print("Waiting for GNSS connection...")
        # Unfortunately, the tuple comparison method - cmp() - is not available in MicroPython
        while(self.gnss.coordinates()[0] == None and self.gnss.coordinates()[1] == None):
            pass

        print("GNSS connection acquired")

    def getLocation(self):
        return self.gnss.coordinates()


class CarTracker:
    def __init__(self, communications, gnss):
        self.communications = communications
        self.gnss = gnss

    def beginTracking(self):
        self.setup()
        while(True):
            self.sendLocationData()

    def setup(self):
        self.gnss.setup()
        for communication in self.communications:
            communication.setup()

    def sendLocationData(self):
        location = self.gnss.getLocation()
        for communication in self.communications:
            communication.send(location)


communications = [ConsoleCommunication()]
gnss = PycomGNSS()

carTracker = CarTracker(communications, gnss)
carTracker.beginTracking()
