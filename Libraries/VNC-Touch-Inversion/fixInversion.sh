#!/bin/bash

cd /home/pi/kivy/kivy/input/providers

sed -i '420s/.*/            invert_y = int(bool(drs("invert_y", 0)))/' hidinput.py

cd /home/pi/kivy

sudo python3 setup.py install
