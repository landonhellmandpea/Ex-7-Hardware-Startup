import os
import pygame
pygame.init()
import RPi.GPIO as GPIO

os.environ['DISPLAY'] = ":0" #UNCOMMENT THIS LINE!!
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.clock import Clock

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.Joystick import Joystick

from pidev.stepper import stepper
from Slush.Devices import L6470Registers

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
EXAMPLE_SCREEN_NAME = 'example'
MOTOR_SCREEN_NAME = 'motor'

joy = Joystick(0, True)

#spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20, steps_per_unit=200, speed=8)

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class ExampleScreen(Screen):

    def transition2(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


class MotorScreen(Screen):

    def transition3(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def pressedMotor(self):
        s0.start_relative_move(5)



class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    joystick_location_x = joy.get_axis("x")
    joystick_location_y = joy.get_axis("y")

    def updateJoy(self, dt):
        joystick_location_x = joy.get_axis("x")
        joystick_location_y = joy.get_axis("y")
        joystick_location_x = round(joystick_location_x * 100)
        joystick_location_y = round(joystick_location_y * -100)
        joystick_coordinates = (joystick_location_x, joystick_location_y)
        self.ids.locationLabelx.text = str(joystick_coordinates)


    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.updateJoy, 0.001)


    def animate(self):
        anim = Animation(x=-100, y=-100) + Animation(x=-100, y=100) + Animation(x=100, y=100) + Animation(x=100, y=-100)
        anim2 = Animation(x=0, y=0)
        if self.ids.test_button.text == 'on':
            anim.repeat = True
            anim.start(self)
        elif self.ids.test_button.text == 'off':
            Animation.cancel_all(self)
            anim2.start(self)


    def transition1(self):
        SCREEN_MANAGER.current = EXAMPLE_SCREEN_NAME

    def transition4(self):
        SCREEN_MANAGER.current = MOTOR_SCREEN_NAME

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        if self.ids.test_button.text == 'on':
            self.ids.test_button.text = 'off'
            self.ids.test_button.color = 1, 0, 0, 1


        else:
            self.ids.test_button.text = 'on'
            self.ids.test_button.color = 0, 1, 0, 1

        print("Callback from MainScreen.pressed()")

    def pressed2(self):

        prior = self.ids.button_counter.text
        prior = int(prior)
        prior += 1
        self.ids.button_counter.text = str(prior)

    def pressed3(self):

        if self.ids.motorLabel.text == 'Motor On':
            self.ids.motorLabel.text = 'Motor Off'

        else:
            self.ids.motorLabel.text = 'Motor On'

    def pressed4(self):

        joystick_location_x = joy.get_axis("x")
        joystick_location_y = joy.get_axis("y")
        joystick_coordinates = (joystick_location_x, joystick_location_y)
        self.ids.locationLabelx.text = str(joystick_coordinates)

    def slide_it(self, *args):
        self.slide_text.text = str(int(args[1]))
        t = int(args[1])
        t = t / 100
        self.ids.slider_label.color = 1, 1, 1, t

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
Builder.load_file('ExampleScreen.kv') #landon make sure to add builder to each kv screen so that you can actually see the damn button...
Builder.load_file('MotorScreen.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ExampleScreen(name=EXAMPLE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(MotorScreen(name=MOTOR_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
    joy = Joystick(0, False)
