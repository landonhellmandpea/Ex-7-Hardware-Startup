# Temperature Sensor

## Overview
[Installing Packages](https://github.com/dpengineering/pyHardwareUnitTesting/tree/master/TemperatureSensor#check-i2c-devices)

[Enabling I2C](https://github.com/dpengineering/pyHardwareUnitTesting/tree/master/TemperatureSensor#enabling-i2c-in-raspberry-pi-configuration)

[Reading Temperature Sensor](https://github.com/dpengineering/pyHardwareUnitTesting/tree/master/TemperatureSensor#reading-from-the-temperature-sensor)

## Installing Necessary Packages
In order to read from the Temperature you need to have the python3 smbus installed
You can do this by running this command in terminal
```sudo apt-get install python3-smbus```
or by running the prewritten [script](../Libraries/TemperatureSensor/installPackages.sh)

## Enabling I2C in Raspberry Pi Configuration
You need to have I2C enabled in the Raspberry Pi Configuration to be able to communicate with the Temperature Sensor
1. Enter ```sudo raspi-config``` in terminal to enter the Raspberry Pi configuration screen
2. Use the arrow keys to go down to number 5 "Interfacing Options"
3. Then down to p5 "I2C"
4. Enter yes to enable
5. Once enabled you can exit the configuration and reboot the pi for the chanes to take effect by running ```sudo reboot```


### Check I2C devices
You can check and see what devices are connected via I2C by running:
```bash
sudo i2cdetect -y 1
```
You should see something in column "8" and row "10" an 18
This means there is a device connected on address 18 through I2C


## Reading from the Temperature Sensor
Reading from the temperature sensor is pretty simple all you need to do is import the Temperature Sensor Class and create a Temperature Sensor object

* You can copy the Temperature Sensor [File](../pidev/TemperatureSensor.py) into your own repository
* Refer to the [example code](../Libraries/TemperatureSensor/main.py) on how to make a Temperature Sensor Object and getting the temperature
