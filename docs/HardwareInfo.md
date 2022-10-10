# SlushEngine

## Hardware Overview

This is the SlushEngine: Model X LT. 

![](https://i.imgur.com/2v12RMR.png?1)

It is a stepper Motor controller with the ability to control 4 steppers, and has an additional 16 General Purpose input/output (GPIO) pins (3.3v)
### Power
Here is where power is attached to the SlushEngine. It can be between 8v-35v.

![](https://i.imgur.com/odr3LFQ.png?1)

### Steppers
These four ports (Motor 0-3)are where you attach the stepper motors to the board. When attaching motors make sure the wires are in the corrrect port (A+,A-,B+,B-). You can find out which wire is which on your steppers datasheer. 

![](https://i.imgur.com/VerCrTt.png?1)

### Limit Switches
There are also four ports where you can attach limit switches (SW0-SW3) to home the steppers (0-3) which can be found here:

![](https://i.imgur.com/g51PaSy.png?1)

### GPIO
The sixteen GPIO pins can be found here, along with ground and 3.3v pins. They are in two rows labeled PA0-PA7, PB0-PB7, and a third row for the 3.3v and ground pins. The pins are all digital.

![](https://i.imgur.com/TVrEYj9.png?1)

### UEXT
There is also a UEXT connector where we can attach i2c, spi, or serial devices. Documentation for this connector can be found [here](https://www.olimex.com/Products/Modules/UEXT/resources/UEXT_rev_B.pdf) 

![](https://i.imgur.com/0ws4Ydz.png?1)

### Raspberry Pi
And finally here is where you attach the Raspberry Pi:

![](https://i.imgur.com/xuiFksD.png?1)


## Software
The easiest way to control the Slush engine is through [stepper.py](https://github.com/dpengineering/RaspberryPiCommon/blob/master/pidev/stepper.py), a wrapper for the slush engines existing library, found in RaspberryPiCommon.
To use the stepper library you need to import it at the top of the file
```
from pidev import stepper

```
Next you need to creat a stepper object for each stepper in your project. You can see all of the constructor options in the code. But the most important ones are port, where the stepper is physically plugged in, speed, how fast the stepper will move, and micro_steps, smoother movement at the cost of torque and max speed (must be in base 2 (1,2,4,8,16,32,64,128))
```
STEPPER = stepper(port=2, speed=500, micro_steps=32)
```
Now you have a wide variety of options for controlling the stepper. They are all well documented in stepper.py so give some a try. Good Luck!

