# Connect to your Raspberry Pi via SSH

You can access the command line of your Pi on another computer using a protocol known as SSH. This is extremely useful if you dont want to connect a keyboard and mouse to your Pi or if you want to execute programs on the Pi from your laptop.

Note that both your Pi and Laptop must be connected to the same network for this to work.

1. Launch `sudo raspi-config` and enable SSH under the interfacing or advanced options pane. Reboot if prompted.
2. Find the ip address of your Pi by running `sudo ip addr show`. Your IP address will be listed under wlan0 > inet if you are connected via wifi. Otherwise it will be listed under eth0. Ignore any numbers after slashes in the address.
3. On the laptop/desktop you are trying to connect with, run `ssh pi@IPADDRESS` where IPADDRESS is the address we just found on the pi. The `pi` is the name of the user. Change this if necessary but it should be pi by default.
    * Note that this command will not work natively on the Windows Command Prompt. To use the `ssh` command on windows, use a bash shell like Git Bash. This should work natively in the terminal of macOS or Linux.
4. Enter the password for the `pi` user if prompted. 
5. Now you can access the shell from your own computer! You can execute any non-ui commands from your computer on the pi. Use a command line editor like vim to edit files directly. Note that UI applications arent supported over SSH.
