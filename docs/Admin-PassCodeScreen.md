# Configuring an Admin Screen

The process of adding an admin screen to your UI is simple.
Getting to the admin screen requires adding the passcode screen which prevents common users from accessing the admin screen.

It is assumed you have created your own AdminScreen.kv with all the admin functionality. Here is a [reference project](https://github.com/dpengineering/SandTablePi2.0)
that implements everything in this guide, use it as a resource if you encounter difficulties.


## Adding the passcode screen
There is a default passcode screen that is already written, and should be used. This ensures standard implementation between projects.
* Make sure you have the most recent version of RaspberryPiCommon cloned and pidev installed
* In your main UI file add the following import statement ```from pidev.kivy import PassCodeScreen```

* This import statement will add a hidden button (very small) in the bottom right corner. NOTE: this will only be added if your main
screen name is "MainScreen" if it is different you need to run a command.

 * Add this line of code to your main UI file, run your project once then you can delete this line ```PassCodeScreen.change_main_screen_name('nameOfMainScreen')```
 This command tells the PassCodeScreen what the name of your main UI screen is. This needs to be run every time you change your mains UI screen name. Once it has been run once you can 
 delete the line.
  
 * Next you need to specify the name of your (already created) admin screen by adding to your main UI code ```PassCodeScreen.set_admin_events_screen('nameOfAdminScreen')```, here is an [example](https://github.com/dpengineering/SandTablePi2.0/blob/17a309b2185e5c54e212d2f488afe4e4fcdc346f/sandtable/ui/GUI.py#L92)
 This line specifies the name of your admin screen which the passcode screen will transition to upon a successful password entry. Here is an [example](https://github.com/dpengineering/SandTablePi2.0/blob/master/sandtable/ui/AdminScreen.kv)
 of an active AdminScreen.kv
 
 * Now you need to specify the name of the screen to transition back to (when the "back to game" button is pressed) by adding the line ```PassCodeScreen.set_transition_back_screen('nameOfScreenToTransitionTo')```, here is 
 an [example](https://github.com/dpengineering/SandTablePi2.0/blob/17a309b2185e5c54e212d2f488afe4e4fcdc346f/sandtable/ui/GUI.py#L93)
 
 * Finally you need to add the PassCodeScreen widget to the screenmanager for example if your screenmanager is named: "SCREEN_MANAGER" you would run 
 ```SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))```, here is an [example](https://github.com/dpengineering/SandTablePi2.0/blob/17a309b2185e5c54e212d2f488afe4e4fcdc346f/sandtable/ui/GUI.py#L128)
 
  * In your main screen class add the following method (change variable naming to fit your project). This method allows the UI to transition from the main screen to the PassCodeScreen.
 ```python
def admin_action(self):
    SCREEN_MANAGER.current = 'passCode' 
``` 
 
 
 ## Conclusion
 After following the steps outlined above there should be a hidden button in the bottom right corner of your main UI screen. Upon press of this button
 it should transition the screen to the passcode screen where if you enter the correct password (7266) it will transition to your admin screen.
 
 ## Troubleshooting
 Here is one [example](https://github.com/dpengineering/RaspberryPiCommon/blob/master/PiKivyProjects/NewProject/main.py) and [another.](https://github.com/dpengineering/SandTablePi2.0/blob/master/sandtable/ui/GUI.py)
 Additionally, there are the docs for [PassCodeScreen](https://dpengineering.github.io/RaspberryPiCommon/classpidev_1_1kivy_1_1_pass_code_screen_1_1_pass_code_screen.html)
 
 If all else fails you can go to [RaspberryPiCommon](https://github.com/dpengineering/RaspberryPiCommon/tree/master/pidev/kivy) and copy the contents of PassCodeScreen.kv and PassCodeScreen.py to
 your projects directory and modify your project to use the projects local version if the pidev version doesn't work.