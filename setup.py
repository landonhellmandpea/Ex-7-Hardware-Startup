from distutils.core import setup

setup(
    name="pidev",
    version='0.1dev',
    packages=["pidev", "pidev.kivy", "pidev.Cyprus_Commands"],
    long_description="A DPEA package containing RPi infrastructure helpers.",
    install_requires=["pyserial", "requests", "smbus", "adafruit-blinka", "adafruit-circuitpython-vl6180x"
                      ]
)
