By default, Raspberry Pi launches a desktop environment on startup.  This is bad for two main reasons:

* Slows down other functionality - Kivy doesn't replace the desktop.  It simply is drawn over it.  When we have both Kivy and the Desktop being drawn/processed, Kivy is noticable slower.

* Still interactive - The default Kivy window provider does not stop touch and keyboard events from propagating to the Desktop.  The most common result of this are re-arranged desktop icons (terrible, I know).  However, it is possible for more dangerous things to happen such as deleting files.  I've also been able to shutdown a pi while a Kivy app is running (tap in bottom left, tap up a little, tap middle of screen).

The solution is rather simple: disable the Desktop.

**When projects are ready to ship or no need longer a desktop, follow the following steps:**

1. `sudo raspi-config`
2. Boot Options
3. Desktop/CLI
4. Console/Autologin
5. Finish and reboot

Kivy projects will continue to work, but there will only be a console behind the Kivy application instead of the full desktop.  Touch events are ignored by the console.

Quitting the Kivy app will reveal this console.  Plug in a keyboard and you can issue commands.  To restore the desktop, repeat the steps above, but select `Desktop/Autologin`.

In rare cases, you may have to update your `launcher.sh` script.  See issue [25](https://github.com/dpengineering/RaspberryPiCommon/issues/25) for more info

_Wifi can easily be changed without the desktop visible.  Look under the `Networking Options` of `raspi-config`._
