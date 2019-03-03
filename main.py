# pylint: disable=import-error

import machine
import math
import network
from network import Sigfox
import socket
import struct
import pycom
import os
import time
import utime
import gc
from machine import Timer   # For the period scheduling of transmissions
from machine import RTC
from L76GNSS import L76GNSS
from pytrack import Pytrack

# Unfortunately, the abstract base class (abc) module is not available in MicroPython
class CommunicationInterface():
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def send(self, coordinates):
        pass


class WiFiCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up WiFi...")
        print("WiFi set up")

    def send(self, coordinates):
        print("Sending: " + str(coordinates))


class SigFoxCommunication(CommunicationInterface):
    # https://docs.pycom.io/firmwareapi/pycom/network/sigfox.html

    def setup(self):
        print("Setting up SigFox...")
        # RCZ1 to specify Europe, Oman & South Africa.
        # RCZ2 for the USA, Mexico & Brazil.
        # RCZ3 for Japan.
        # RCZ4 for Australia, New Zealand, Singapore, Taiwan, Hong Kong, Colombia & Argentina.
        sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
        self.sigfoxSocket = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
        self.sigfoxSocket.setblocking(True)
        self.sigfoxSocket.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        print("SigFox set up")

    def send(self, coordinates):
        dataToSend = struct.pack('>II', int(coordinates[0]*100000),  int(coordinates[1]*100000))
        print("Sending: " + str(coordinates) + " over SigFox as " + str(dataToSend) + "(" + str(len(dataToSend)) + " bytes)...")

        # Maximum data size is 12 bytes
        # Up to 140 messages per day
        pycom.rgbled(0xff00)
        self.sigfoxSocket.send(dataToSend)
        pycom.rgbled(0)

        print("Sent")


class CellularCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up Cellular...")
        print("Cellular set up...")

    def send(self, coordinates):
        print("Sending: " + str(coordinates))


class ConsoleCommunication(CommunicationInterface):
    def setup(self):
        print("Setting up console...")
        print("Console set up...")

    def send(self, coordinates):
        print("Sending: " + str(coordinates))
        print("{}".format(coordinates))


# Unfortunately, the abstract base class (abc) module is not available in MicroPython
class GNSSInterface():
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def getCoordinates(self):
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

    def getCoordinates(self):
        return self.gnss.coordinates()


class CarTracker:
    def __init__(self, communications, gnss, updateRate):
        self.communications = communications
        self.gnss = gnss
        self.__alarm = Timer.Alarm(handler=None, s=updateRate, periodic=True)

    def beginTracking(self):
        self.setup()
        self.__alarm.callback(handler=self.alarmCallback, arg=None)

    def setup(self):
        self.gnss.setup()
        for communication in self.communications:
            communication.setup()

    def alarmCallback(self, alarm):
        self.sendLocationData()

    def sendLocationData(self):
        coordinates = self.gnss.getCoordinates()
        for communication in self.communications:
            communication.send(coordinates)

pycom.heartbeat(False)
pycom.rgbled(0xFFBF00)

communications = [SigFoxCommunication()]
gnss = PycomGNSS()
updateRate = 60 # Seconds

carTracker = CarTracker(communications, gnss, updateRate)
carTracker.beginTracking()
