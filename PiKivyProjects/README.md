# Creating a UI With Kivy on the Raspberry Pi

This document assumes that you have a Raspberry Pi with a working image received from the DPEA

All python code referenced below will be in Python 3.5 or above.

## Kivy Overview
Kivy is a UI library that makes it easy to create UIs that are written in 100% Python. It is organized in a hierarchical parent/child system. Most programs written in Kivy will have 2 basic files, ```main.py``` and ```main.kv```. ```main.py``` is where all of the actual Python programming is done. The ```.kv``` file is where all layout information will be stored. This includes information like the location and size of widgets (Buttons, Images, Labels, etc...), what they do and where they are in the hierarchy. 

### App Class

The highest object on the widget hierarchy will be the App. This object requires little to no customization for our purposes. It will be declared in your .py file like this:
```
class MyApp(App):
    def build(self):
        return SCREEN_MANAGER
```

In order to begin your application, the ```main.py``` file must also include the following lines:

```
if __name__ == "__main__":
    MyApp().run()
```

'MyApp' can be renamed to whatever you want.

### Screen Manager

The next object embedded inside the App will be the Screen Manager. This is an object that manages every screen for your app. meaning that it handles all of the transitions and screen navigation for your App. It should be declared as a global variable:
```
SCREEN_MANAGER = ScreenManager()
```

### Screens

Screens are where most of your programming will be done. While your app is running, the UI will be occupied by one screen at a time. This screen will have buttons, labels, and other types of objects that the user will be able to interact with. To create a custom screen, you will need to edit both the ```.py``` file and the ```.kv``` file. To start, open the ```.kv``` file and add this:

```
<MainScreen>:   
    name: 'main'
    FloatLayout:
        size_hint: None, None  
```

This block of code will define a new screen called ```MainScreen``` with the name ```'main'```. You can later use this name to reference this particular screen (for example, when transitioning to it). This block of code (the line formatted like ```<SomeClass>:``` and everything directly below it that is indented) is known as a class rule in the kv language and defines the appearance and behavior of the class (```SomeClass```, in this case).

```FloatLayout``` is the most basic layout type we will use. The layout type basically controls how objects are moved when the screen size changes. Since our screen sizes are relatively constant, we usually use the FloatLayout, which allows us to place objects in a X,Y coordinate system. 
Information on other layouts may be found [here.](https://kivy.org/docs/gettingstarted/layouts.html)

Now you can add this screen to the screen manager in the ```.py``` file. For example:
```
SCREEN_MANAGER.add_widget(MainScreen(name='main'))
```
where ```MainScreen``` is replaced with the screen's class name and ```'main'``` is replaced with the name of the screen, which should match the name defined in the ```.kv``` file (see above).

Most likely, this screen will contain buttons or other objects that will have something happen upon an event occurring (like tapping or dragging). In order to handle these events, there must be a place to declare the functions that handle them in your ```.py``` file. This is done by creating a new class like this in your ```.py``` file:

```
class MainScreen(Screen): 
    def do_nothing(self):
        pass
```

This block of code will create a new class with the name ```MainScreen```. Note that this name is the same as the name in the <> of the ```.kv``` file and NOT the ```name:``` property. You can think of this class in the ```.py``` file and the class rule in the ```.kv``` file as one and the same. In this example, there is one function called ```do_nothing``` which does nothing. We can attach this function to a button press or similar event (see example below).

### Widgets

Widgets are the building blocks with which you will build your UI. Widgets include Buttons, Sliders, Labels, and various other things which can be found [here](https://kivy.org/docs/api-kivy.uix.html) under UX widgets. 

You will add widgets into your ```.kv``` file like so

```
Button:
    text: 'I am a Button'
    size_hint: None, None
    size: 200, 100
    x: root.width - self.width -500
    y: root.height * .45
    background_color: .1, .1, 1 ,1
    on_release: root.do_nothing()
 ```
 This block of code declares a button and gives it all of its properties.
 
 ```text``` is the text displayed on the button.
 ```size_hint: None, None``` allows us to assign an absolute size to our widget
 
 ```size``` is the size in pixels
 
 Positioning is done in cartesian coordinates where the origin in the bottom left of the screen, ```x``` gives x position, and ```y``` gives y position.
 
 ```background_color``` is the color of the button in R, G, B, alpha, where these parameters all range from 0 to 1. Alpha is sort of like opacity.
 
 ```on_release: root.do_nothing()``` binds a function to a button on a button event (tap/release). This function is declared in your ```.py``` file under the class for this screen. 

More information on widget properties can be found [here](https://kivy.org/docs/api-kivy.uix.widget.html)

### Parent/Child Formatting

A very important part of Kivy is parent child relationships. These define what information widgets have access to and what widgets can communicate with each other. 

```
<MainScreen>:
    name: 'main'
    FloatLayout:
        size_hint: None, None 
        
        Button:
            size_hint: None, None
            text: 'Begin'
            font_size: 20
            size: self.parent.size
            background_color: .1, .1 ,1 ,1
            center: root.center
            on_release: root.do_nothing()
```            

In this example we have our screen ```main``` with a child ```FloatLayout```. Next we have the ```Button``` which is a child of ```FloatLayout```. In the properties we can see a few new lines referencing ```parent``` and ```root```.

 ```size: self.parent.size``` sets the size of the button to the size of its parent, which is the ```FloatLayout``` in this example. 

 ```center: root.center``` sets the center of the widget to the center of its root, which is ```<MainScreen>``` in this example, and ```on_release: root.do_nothing()``` calls the ```do_nothing()``` function of ```MainScreen``` in the ```.py``` file. Remember that? Here it is again:

```
class MainScreen(Screen): 
    def do_nothing(self):
        pass
```

For the most part you will just be getting size or position from the parent widget, or calling functions from root. But you can also use this to access data from your ```.py``` file like in this example.   

```
<MainScreen>:
    name: 'main'
    FloatLayout:
        size_hint: None, None 
        
        Button:
            size_hint: None, None
            text: 'Begin'
            font_size: 20
            size: self.parent.size
            background_color: .1, .1 ,1 ,1
            center: root.center
            on_release: self.text = root.button_text
```

In this case the text of the label is being set to the variable ```button_text``` from the ```MainScreen``` class, which would now look like this in the ```.py``` file:

```
class MainScreen(Screen): 
    def do_nothing(self):
        pass
    button_text = 'This is a Button'
```

Another important thing to notice is the ```self.``` in front of calls to parent (as in ```size: self.parent.size``` in the example above). This is telling the code to reference the current widget. We also sometimes use it when referencing the widget's attributes, as in ```on_release: self.text = root.button_text```. However, we do not write ```self.root``` because ```root``` always refers to the base widget of any rule, no matter what. We also do not write ```self.text: 'Begin'``` because the kv language understands that we are changing the ```Button```'s attributes here.

### Examples

For an example please reference the NewProject example that can be found [here.](https://github.com/dpengineering/RaspberryPiCommon/tree/master/PiKivyProjects/NewProject)
