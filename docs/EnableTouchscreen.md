## Instructions to enable Kivy touchscreen:

1. Run any Kivy code. Use Control+C to exit the program (since touchscreen will not be functioning).

2. Navigate to `~/kivy` and open `.kivy`'s `config.ini` with nano:
```
$ cd ~/kivy
$ nano ~/.kivy/config.ini
````
3. In the `[input]` section, remove the existing lines and put in:
```
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

*From https://github.com/mrichardson23/rpi-kivy-screen/blob/master/README.md*
