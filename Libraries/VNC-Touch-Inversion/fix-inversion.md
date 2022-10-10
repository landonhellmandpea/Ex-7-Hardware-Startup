# Fixing Kivy touch inversion when using VNC

## Attempt to run the auto script
There is a script to fix the issue, however it may not work depending on where the Kivy package was installed
Double-click on fixInversion.sh and choose to execute in terminal. If successful this should take a few minutes. If not proceed to Manually Fixing

## Manually Fixing
On the Raspberry Pi navigate to kivy/kivy/input/providers and open up hidinput.py, and scroll to line 420.

The line should read ``` invert_y = int(bool(drs('invert_y', 1))) ``` replace the line with ``` invert_y = int(bool(drs('invert_y', 0))) ```
Save the file.

## Rerun setup.py
Once the hidinput.pt has been edited navigate to kivy/ in the terminal(go back a few directories). There should be a setup.py in the main kivy directory.
When you are in the correct directory run the command ``` sudo python3 setup.py install ``` this will reinstall kivy. This tends to take a while.

## Test
This should fix the issue, now you should launch a Kivy aplication and double check that all is well.
