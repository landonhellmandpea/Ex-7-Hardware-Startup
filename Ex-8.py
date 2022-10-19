import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()

import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)

cyprus.initialize()
cyprus.setup_servo(1)
cyprus.set_servo_position(1, 0)
sleep(1)
cyprus.set_servo_position(1, 1)
sleep(1)
cyprus.close()


#LimitSwitch = 3
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(LimitSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
#if GPIO.input(LimitSwitch) == 3:
#    print('Hello')
#else:
#    print('goodbye')




