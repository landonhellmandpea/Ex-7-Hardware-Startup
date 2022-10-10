# Kivy UI Libraries for the DPEA
This document assumes that you have the most recent version of pidev (python module found [here](https://github.com/dpengineering/RaspberryPiCommon)) installed.
Documentation for pidev can be found [here.](https://dpengineering.github.io/RaspberryPiCommon/)

These are the libraries to be used for all Mechatronics projects that require the use of Python with Kivy.
Please refer to this doc, [auto-generated docs](https://dpengineering.github.io/RaspberryPiCommon/), as well as reading through the code files.

Before using these libraries, make sure you have these imports in your python file:

## DPEAButton

A button that's a colored, rounded rectangle with a drop shadow. Text has a bolded white body and a black outline.

### Required Setup
To use you must import it from pidev:
```python
from pidev.kivy import DPEAButton
```

### Appearance Customization

You can specify the ```text```, ```color```, ```size```, ```center_x```, and ```center_y```. Here's an example of what a DPEAButton looks like written in the kv file:
```
DPEAButton:
    background_color: 0, 0, 0, 0
    background_normal: ''
    size_hint: None, None
    text: 'Hello World!'
    size: 40, 40
    center_x: root.width * 0.97
    center_y: root.height * 0.955
    color: 1, 0, 0, 1
```

The parameters for ```color``` are red, green, blue, alpha (think of alpha as opacity), so in this case, a bright red.

### Touch Event Handling
In order for the button to respond to events you must specify the ```on_touch_down``` parameter to bind to a function defined in the screens python code.
You can also set the ```id``` parameter which is especially important as it can be used later to change any characteristic of the button.
Here's an example of what your kivy code should look like now:
```
DPEAButton:
    id: ExampleButton
    size_hint: None, None
    text: 'Hello World!'
    size: 40, 40
    center_x: root.width * 0.97
    center_y: root.height * 0.955
    color: 1, 0, 0, 1
    on_touch_down: root.ExampleButtonDown()
```

## Image Button

An Image with button-like behavior since kivy unfortunately does not have a default ```ImageButton``` class.

### Required Setup

At the top of your file with your import statements, add ```from pidev.kivy import ImageButton```. To use the ```ImageButton```, simply initialize it in your kivy file like so:
```
ImageButton:
    source: "path_to_image"
    center_x: root.width * 0.5
    center_y: root.height * 0.5
```

## Pause Scene
There are instances when we want to have a pause screen while the project is performing an action.
This is achieved by using the PauseScreen.

### Pause Scene Setup
First import the pause screen:
```python
from pidev.kivy.PauseScreen import PauseScreen
```

### Usage

To use the pause scene, simply call the pause method like so:
```PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Pause", pause_duration=10)```

Please refer to the [documentation](https://dpengineering.github.io/RaspberryPiCommon/classpidev_1_1kivy_1_1_pause_screen_1_1_pause_screen.html) for more information on the parameters.

## PassCodeScreen and AdminScreen

Please refer to these [instructions](https://github.com/dpengineering/RaspberryPiCommon/blob/master/docs/Admin-PassCodeScreen.md) on how to configure your Passcode and Admin screens.
