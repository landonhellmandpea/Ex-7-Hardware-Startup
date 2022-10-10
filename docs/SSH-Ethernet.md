# Setting up SSH Over Ethernet

This setup entails how to setup your Linux PC (currently tested on Ubuntu) to ssh over ethernet with the Raspberry Pi Images used at the DPEA.

## Instructions
Begin by powering on the Raspberry Pi and connecting to your PC via an ethernet cable.

On Ubuntu open the settings and navigate to wired settings. Verify the connection is switched to on and click the settings wheel next to the toggle on switch.
Select "IPv4" from the top menu and select the "Manual" IPv4 method.

Under Addresses table entry enter the following address: 172.17.21.1
Under Addresses table entry enter the following Netmask: 255.255.0.0

Under DNS add the following DNS entries: 172.17.17.4, 10.7.2.60

Lastly at the bottom of the page toggle on "Use this connection only for resources on its network"

Reboot your PC to ensure the changes go into effect.

## Connecting to the Pi
After completing the above instructions you should be able to SSH into your Raspberry Pi by running
```ssh pi@172.17.21.2``` in terminal.

You should be greeted with the option to enter the password of the Pi.
Once this is complete you can copy your ssh key of your PC to the Pi for easier login by running ```ssh-copy-id pi@172.17.21.2```

## Note
This setup needs to be done every time a new USB dongle is used with your PC.
