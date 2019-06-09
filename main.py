# pylint: disable=import-error

import machine
import math
import network
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
        sigfox = network.Sigfox(mode=network.Sigfox.SIGFOX, rcz=network.Sigfox.RCZ1)
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
        self.sendLocationData()
        self.__alarm.callback(handler=self.alarmCallback, arg=None)

    def setup(self):
        # Turn off network services that are not needed
        network.Bluetooth().deinit()
        network.WLAN().deinit()
        network.LTE().deinit()

        self.gnss.setup()
        for communication in self.communications:
            communication.setup()

    def logCoordinates(self, datetime, coordinates):
        with open("/flash/locations.txt", "a+") as location_file:
            # 2019-05-22 11:41:19 (51.80332, -0.17852)
            location_file.write(str(datetime) + " " + str(coordinates) + "\n")
        # To read the written data:
        #   with open("/flash/locations.txt", "r+") as locations_file:
        #       locations_file.read().split("\n")
        # TODO: Check that the file system does not get full, delete oldest/first lines from file if this happens
        #   Useful commands to do this: 
        #       os.getfree("/flash") # in KiB? e.g. 4036
        #       os.listdir("/flash")
        #       os.stat("/flash/main.py") # 7 tuple is size in bytes e.g. 4345 bytes = 4 KB

    def alarmCallback(self, alarm):
        self.sendLocationData()

    def sendLocationData(self):
        coordinates = self.gnss.getCoordinates()
        for communication in self.communications:
            communication.send(coordinates)
            # The GNSS system will know the datetime, but the Pycom library does not expose this. The device
            # itself has no concent of time, other than local time, which isn't useful. 
            self.logCoordinates("???", coordinates)

pycom.heartbeat(False)
pycom.rgbled(0xFFBF00)

communications = [SigFoxCommunication()]
gnss = PycomGNSS()
updateRate = 30 # Seconds (should be 600 = 10 minutes)

carTracker = CarTracker(communications, gnss, updateRate)
carTracker.beginTracking()
