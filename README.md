# GPS Tracker

A project to create a GPS tracking device with no monthly costs. Uses a Pycom [fipy](https://pycom.io/product/fipy/) and [pytrack](https://pycom.io/product/pytrack/). 

The idea is for the GPS tracker to be placed inside a vehicle and when the vehicle starts up the tracker searches for an approved mobile telephone over Bluetooth. If the phone cannot be found, it assumes that the car is being stolen, alerts the user and begins tracking the car.

There is an additional option to include a small battery such that the tracker can send a last reading when the vehicle's ignition is turned off. This would also allow potential use of the built-in accelerator to trigger a GPS message when movement is detected e.g. if the vehicle is being towed (the ignition wouldn't be on).

## Usage
1. Using Visual Studio, install the Pymakr plugin
2. Connect the pytrack with attached fipy to the computer
3. Open the code in Visual Studio
4. Right click on one of the project files and click upload

## Functionality
### GPS
Basic GPS readout has been implemented using [Pycom's libraries and examples](https://github.com/pycom/pycom-libraries/tree/master/pytrack).

- The date printed is incorrect (1970), could this not be acquired from the GPS connection?
- The Pycom library only supplies coordinates and time, other libraries may give more information such as accuracy and altitude
- Why does the Pycom example need to setup an RTC beforehand?
- Why does the Pycom example use the `gc` library?

### Bluetooth
TODO

### Communications
The plan is to use SigFox until the UK's IOT LTE network capability is ready, then switch to using a Hologram.io SIM card. Communication rate will be limited as there are restrictions on the amount of data that can be send over these networks over a given time period. 

TODO

### Monitoring
The plan is to use either the free tier of Microsoft Azure IoT Central, or the Pybytes platform to view data sent from the Pycom boards, track the position of them and to send out alerts. The monitoring/tracking should be shareable, so, for example, the Police can use it to recover the stolen vehicle. 

TODO
