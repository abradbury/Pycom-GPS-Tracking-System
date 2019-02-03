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

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pytrack()
l76 = L76GNSS(py, timeout=30)

while (True):
    coord = l76.coordinates()
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
