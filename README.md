# GPS Tracker

An exploratory project with the aim of creating a GPS tracking device with no monthly costs. 

The idea is for the GPS tracker to be placed inside a vehicle and when the vehicle starts up the tracker searches for an approved mobile telephone over Bluetooth. If the phone cannot be found, it assumes that the car is being stolen, alerts the user and begins tracking the car.

There is an additional option to include a small battery such that the tracker can send a last reading when the vehicle's ignition is turned off. This would also allow potential use of the built-in accelerator to trigger a GPS message when movement is detected e.g. if the vehicle is being towed (the ignition wouldn't be on).

## Usage
1. Using Visual Studio, install the Pymakr plugin
2. Connect the pytrack with attached FiPy to the computer
3. Open the code in Visual Studio
4. Right click on one of the project files and click upload

## Components
* [Pycom FiPy](https://pycom.io/product/fipy/) (when the UK's IOT LTE network capability is ready, then a [Pycom GPy](https://pycom.io/product/gpy/) can be used instead, as it is cheaper)
* [Pycom pytrack](https://pycom.io/product/pytrack/) (includes GNSS capabilities and an accelerometer)
* Sigfox antenna
* Cellular antenna
* A case/box such as the [Pycase](https://pycom.io/product/pycase-clear/)
* A "hard-wire kit" to connect the tracker to your car's fuse box, for example, [the Nextbase one](https://www.amazon.co.uk/Nextbase-Camera-Hard-Wire-Kit/dp/B00XHYSQAC) (but you would need a Micro USB to Mini USB converter/adapter as Nextbase DashCams have a Mini USB input, but Pycom boards have Micro USB)

Total component cost: around £100

Total monthly cost: £0

## Functionality
### GPS
Basic GPS readout has been implemented using [Pycom's libraries and examples](https://github.com/pycom/pycom-libraries/tree/master/pytrack).

- The date printed is incorrect (1970), could this not be acquired from the GPS connection?
- The Pycom library only supplies coordinates and time, other libraries may give more information such as accuracy and altitude
- Why does the Pycom example need to setup an RTC beforehand?
- Why does the Pycom example use the `gc` library?

### Bluetooth
TODO

[Pycom Bluetooth API](https://docs.pycom.io/firmwareapi/pycom/network/bluetooth/)
[Pycom Bluetooth tutorial](https://docs.pycom.io/tutorials/all/ble.html)

It does not seem possible to uniquely identify an (iOS) phone using Bluetooth Low Energy, as this sort of thing is discouraged for privacy reasons. The advertised MAC address randomly changes. Cannot connect using the actual MAC address. It is possible to *temperamentally* list the services and characteristics the device offers. One possible solution would be to create an iOS app that sets some specific service UUID to search for, but there is some doubt over this as well.

### Communications

[Pycom SigFox API](https://docs.pycom.io/firmwareapi/pycom/network/sigfox.html)
[Pycom SigFox tutorial](https://docs.pycom.io/tutorials/sigfox.html)

The plan is to use SigFox until the UK's IOT LTE network capability is ready, then switch to using a Hologram.io SIM card. Communication rate will be limited as there are restrictions on the amount of data that can be send over these networks over a given time period. 

- The SigFox connection is disappointingly poor where the car will be mainly based, with only 1 in 30 messages getting through, though elevation helps
- To address this, have the SigFox server respond when a message is received - if it can (only 4 downlink messages a day are allowed), then the tracker can stop transmitting, unless the owner intervenes and would like to track the vehicle
- Get callbacks/scheduling working

- The SigFox limit is a regulatory limit, specifically 6 messages per hour
- Downlink messages can only be sent when requested by the device
- The simplest option, for now, would be to have the device continually transmit - but for more use, a battery should be added
  - SigFox TX: 42 mA, idle: 62.7 mA, deep sleep: 24 uA
  - How to enter deep sleep?
  - How to measure voltage/current usage?

### Monitoring
The plan is to use either the free tier of Microsoft Azure IoT Central, or the Pybytes platform to view data sent from the Pycom boards, track the position of them and to send out alerts. The monitoring/tracking should be shareable, so, for example, the Police can use it to recover the stolen vehicle. 

TODO
