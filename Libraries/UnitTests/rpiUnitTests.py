# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
import spidev
import argparse
import time
from time import sleep
from datetime import datetime
import random

import RPi.GPIO as GPIO 
from pidev import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
import Slush

MAX_SPEED = 50
CLOCKWISE = 0
COUNTERCLOCKWISE = 1

DIRECTIONS = ["CLOCKWISE", "COUNTERCLOCKWISE"]

parser = argparse.ArgumentParser()
parser.add_argument("-motor", type=int, help="Enter the motor to test", nargs='?', default = -1)
parser.add_argument("-motorCount", type=int, help="Enter the number of motors to test", nargs='?', default = 4)
parser.add_argument("-verbose", type=bool, help="Print verbose messages", nargs='?', default = True)
parser.add_argument("-value", type=int, help="set value for PWM", nargs='?', default = 100)
parser.add_argument("-position", type=float, help="set position for servo", nargs='?', default = 0.5)
parser.add_argument("-speed", type=int, help="set speed of servo", nargs='?', default = 50)
args = parser.parse_args()

if (args.motor != -1):
    args.motorCount = 0
    
def initTests():
    cyprus.initialize()

def homeTest(motorNumber):
    printTitle(getFunctionName() + " for motor " + str(motorNumber))
    motor = stepper(port = motorNumber, speed = MAX_SPEED/2, micro_steps = 2)
    motor.resetDev()
        
    moveOffSwitch(motor, COUNTERCLOCKWISE)
    
    ### Move motor to random position
    random.seed(datetime.now())
    randPosition = random.randint(100, 1000)
    motor.go_to_position(randPosition)
    
    debug("Stepper HOMING in the Clockwise direction.")
    moveOffSwitch(motor, COUNTERCLOCKWISE)
    motor.home(COUNTERCLOCKWISE)

    port, channel, portChannel = getEncoderInfo(motorNumber)
    homePosition = readEncoder(port, channel)
    debug("Home Position: " + hex(homePosition))
    
    debug("Stepper HOMING in the Counter Clockwise direction.")
    motor.run(CLOCKWISE, MAX_SPEED*4)
    sleep(1)
    motor.stop()
    motor.goHome()
    sleep(0.75)

    lastPosition = readEncoder(port, channel)
    debug("Last Position: " + hex(lastPosition))
    debug("Delta Position: " + hex(motorPositionDelta(homePosition, lastPosition)))
    assertTrue(assertEqualsWithDelta(homePosition, lastPosition, 0x10),
               "Home Test. Encoder value is not at the home position.")
    freeMotor(motorNumber)

def speedTest(motorNumber):
    printTitle(getFunctionName() + " for motor " + str(motorNumber))
    debug("Increase speed in 5 increaments")
    motor = stepper(port = motorNumber, speed = MAX_SPEED)

    for speed in range(100, 600, 100):
        debug("Speed = " + str(speed))
        motor.run(1, speed)
        sleep(2)
        #assertTrue(testSwitch(motor), "speedTest motor " + str(motorNumber))
        #freeMotor(motorNumber)
        
def gpioInputTest():
    printTitle(getFunctionName() + " for A and B output")
    setGPIOValue(True)
    sleep(0.1)
    checkGPIOValue(True)
    setGPIOValue(False)
    sleep(0.1)
    checkGPIOValue(False)

def readEncoderTest(motorNumber):
    port, channel, portChannel = getEncoderInfo(motorNumber)
    encoder = readEncoder(port, channel)
    print("Encoder: " + hex(encoder))

def encoderTest(motorNumber):
    port, channel, portChannel = getEncoderInfo(motorNumber)
    
    printTitle(getFunctionName() + " " + portChannel)
    encoder1 = readEncoder(port, channel)
              
    motor = stepper(port = motorNumber, speed = MAX_SPEED)
    motor.relative_move(-1.0)

    if (encoder1 == 0xffff):
        assertTrue(False, "Encoder " + portChannel + " not connected.")
        return
    
    motor.hardStop()
    motor.relative_move(1.0)
    motor.hardStop()

    encoder2 = readEncoder(port, channel)
    result = motorPositionDelta(encoder1, encoder2)

    debug("Initial Encoder Value: " + hex(encoder1) + " End Encoder Value: " + hex(encoder2) + " Difference: " + hex(result))
    
    # Adjust for the rolling over of the encoder
    result = motorPositionDelta(encoder1, encoder2)

    assertTrue(assertEqualsWithDelta(encoder1, encoder2, 0x30),
               "Encoder Test " + portChannel + " Failed! Out of range (difference should be less than 0x30)")
    cyprus.reset_all_encoder_triggers()

def encoderTriggerTest(motorNumber, value):
    port, channel, portChannel = getEncoderInfo(motorNumber)   
    printTitle(getFunctionName() + " on port: " + portChannel + " with value: " + hex(value))
    
    motor = stepper(port = motorNumber, speed = 10)
    motor.relative_move(1)
    
    cyprus.set_encoder_trigger(channel, value)

    motor.relative_move(50)
    result = readEncoder(port, channel)
    debug("Encoder value: " + hex(result))
    
    assertTrue(assertEqualsWithDelta(value, result, 0x10),
               getFunctionName() + ", expected: " + hex(value) + " actual: " + hex(result) + ". Not within range 0x10")
    cyprus.reset_all_encoder_triggers()
    freeMotor(motorNumber)

def encoderTriggerAutoResetTest(motorNumber, value):
    port, channel, portChannel = getEncoderInfo(motorNumber)
    printTitle(getFunctionName() + " on port: " + portChannel + " with value: " + hex(value))
    
    motor = stepper(port = motorNumber, speed = 10)
    motor.relative_move(1)
    
    cyprus.set_encoder_trigger_auto_reset(channel, value)

    motor.relative_move(50)
    result = readEncoder(port, channel)
    debug("Encoder value for motor " + str(motorNumber) + " is " + hex(result))
    
    assertTrue(assertEqualsWithDelta(value, result, 0x10),
               getFunctionName() + ", expected: " + hex(value) + " actual: " + hex(result) + ". Not within range 0x10")
    
    motor.relative_move(40)

    result = readEncoder(port, channel)
    debug("Encoder value after auto reset: " + hex(result))
    assertTrue(assertDoesNotEqualsWithDelta(value, result, 0x10), "Trigger did not reset on " + portChannel)
    cyprus.reset_all_encoder_triggers()
    freeMotor(motorNumber)

def encoderTriggerRadiusTest(motorNumber, radius, value):
    port, channel, portChannel = getEncoderInfo(motorNumber)   
    printTitle(getFunctionName() + " on port: " + portChannel + " with value: " + hex(value))
    
    motor = stepper(port = motorNumber, speed = 10)
    motor.relative_move(1)
    
    cyprus.set_encoder_trigger(channel, value)
    sleep(1)
    cyprus.set_trigger_radius(channel, radius)

    motor.relative_move(50)
    result = readEncoder(port, channel)
    debug("Encoder value: " + hex(result))
    
    assertTrue(assertEqualsWithDelta(value, result, radius + 0x10),
               getFunctionName() + ", expected: " + hex(value) + " actual: " + hex(result) + ". " + 
               hex(value-result) + " not within range 0x10")
    cyprus.reset_all_encoder_triggers()
    freeMotor(motorNumber)

def relativeMoveTest(motorNumber, value):
    printTitle(getFunctionName() + " motor " + str(motorNumber) + " with value = " + str(value))
    motor = stepper(port = motorNumber, speed = MAX_SPEED)
    debug("Relative move Counter Clockwise.")
    sleep(0.1)
    port, channel, portChannel = getEncoderInfo(motorNumber)
    startPosition = readEncoder(port, channel)
    motor.relative_move(value)
    debug("Relative move Clockwise.")
    sleep(0.1)
    motor.relative_move(-value)
    
    endPosition = readEncoder(port, channel)
    delta = motorPositionDelta(startPosition, endPosition)
    
    debug("Start Position: " + hex(startPosition) +
          ", End Position: " + hex(endPosition) +
          ", Delta: " + hex(delta))

    assertTrue(assertEqualsWithDelta(startPosition, endPosition, 0x10),
               getFunctionName() + " for motor " + str(motorNumber) + ". Start and end position are not the same.")
    motor.stop()
    
#################### PWM Tests #############################
    
def pwmAndStepperTest(pwmPort, stepperPort):
    printTitle(getFunctionName() + " PWM(port = " + str(pwmPort) + ") and Stepper(port = " + str(stepperPort) + ")")
    motor = stepper(port = stepperPort, speed = MAX_SPEED)

    debug("Stepper Run Until Stop for 2 seconds. NOTE: PWM should not be running.")
    motor.run(1, 500)
    sleep(2)
    motor.stop()
    debug("PWM 4000 for 2 seconds")
    cyprus.write_pwm(stepperPort, cyprus.PERIOD, 1000)
    sleep(2)
    debug("Stop PWM")
    cyprus.write_pwm(stepperPort, "period", 0)
    sleep(1)

def testSetServoPosition(pwmPort):
    printTitle(getFunctionName() + " PWM(port = " + str(pwmPort) + ")")
    debug("Connect positional servo to port " + str(pwmPort))
    cyprus.setup_servo(pwmPort)

    debug("Set the position of the servo to start, middle and end positions.")
    for i in range(1, 5, 1):
        cyprus.set_servo_position(pwmPort, 0.0)
        sleep(1)
        cyprus.set_servo_position(pwmPort, 0.5)
        sleep(1)
        cyprus.set_servo_position(pwmPort, 1.0)
        sleep(1)

    cyprus.set_servo_position(pwmPort, 0.0)

def testSetServoSpeed(pwmPort):
    printTitle(getFunctionName() + " PWM(port = " + str(pwmPort) + ")")
    debug("Connect continuous servo to port " + str(pwmPort))
    cyprus.setup_servo(pwmPort)

    debug("Set the 20 speeds of the servo. 10 in one direction and 10 in the other.")
    for i in range(-10, 11, 1):
        cyprus.set_servo_speed(pwmPort, i/10)
        sleep(1)

    cyprus.set_servo_speed(pwmPort, 0.0)

def testSetPWMValues(pwmPort):
    printTitle(getFunctionName() + " PWM(port = " + str(pwmPort) + ")")
    debug("Connect motor controller with DC motor to port " + str(pwmPort))

    period = 50000
    for i in range(0, period+5000, 5000):
        debug("Setting duty cycle to " + str(int((i/period)*100)) + "%")
        cyprus.set_pwm_values(pwmPort, period, i)
        sleep(1)

    cyprus.set_pwm_values(pwmPort, period, 0)

########### Helpers Methods ###########################
    
def setGPIOValue(value):
    slushEngine = Slush.sBoard()

    for i in range(0, 2): 
        label = ("A", "B")[i == 1]
        for j in range(0, 8):
            port = label + str(j)
            debug("Setting " + str(i) + ", " + str(j) + " to " + str(value))
            slushEngine.setIOState(i, j, value)
            sleep(0.05)

def checkGPIOValue(value):
    slushEngine = Slush.sBoard()

    for i in range(0, 2): 
        label = ("A", "B")[i == 1]
        for j in range(0, 8):
            port = label + str(j)
            state = slushEngine.getIOState(i, j)
            debug("Getting " + str(i) + ", " + str(j) + " with value of " + str(state))
            debug(port + " Expected: " + str(value) + ", Received : " + str(state))
            assertTrue(state == value,
                       port + " should be " + str(value) + " but is " + str(state))
            sleep(0.05)

def moveOffSwitch(motor, direction):
    if (motor.read_switch() == 1):
        debug("Moving off switch.")
        motor.run(direction, 100)
        sleep(0.4)
        motor.stop()
        
def readEncoder(port, index):
    sleep(0.1)
    encoderValue = cyprus.read_encoder(port, index)
    return(encoderValue)

def getEncoderInfo(motorNumber):
    if motorNumber == 0:
        port = 1
        channel = 0
    elif motorNumber == 1:
        port = 1
        channel = 1
    elif motorNumber == 2:
        port = 1
        channel = 2
    elif motorNumber == 3:
        port = 2
        channel = 0
        
    portChannel = motorEncoderMessage(motorNumber, port, channel)

    return port, channel, portChannel

def motorPositionDelta(start, end):
    result = end - start
    
    if (result < 0):
        result = start - end
        
    #result = (0xfff - start) + end

    return result

def testSwitch(motor):
    switchSet = False
    for i in range(1, 20, 1):
        switchSet = switchSet|(motor.read_switch() == 1)
        sleep(0.01)
    return switchSet

################## Assert Helpers #################

def assertEqualsWithDelta(expected, result, delta):
    if (result >= expected - delta):
        if (result <= expected + delta):
            return True
    return False

def assertDoesNotEqualsWithDelta(expected, result, delta):
    if (result >= expected - delta):
        if (result <= expected + delta):
            return False
    return True

def assertTrue(condition, message, errorOnly = True):
    if (condition == True):
        if (errorOnly != True): 
            printPassed(message)
    else:
        printFailed(message)

################## Print Helpers #################

def motorEncoderMessage(motorNumber, port, channel):
    return "motor " + str(motorNumber) + ", port " + str(port) + ", channel " + str(channel)

def printTitle(message):
    print("\033[1;33;40m########### %50s ###########" % message)
    print("\033[0;37;40m")
    
def printFailed(message):
    print("\033[1;31;40m##### Failed: " + message)
    print("\033[0;37;40m")

def printPassed(message):
    print("\033[1;32;40m##### Passed: " + message)
    print("\033[0;37;40m")

def debug(message):
    if (args.verbose == True):
        print("# " + message)

def getTestName():
    return sys._getframe().f_code.co_name

def freeMotor(motorNumber):
    motor = stepper(port = motorNumber, speed = 10)
    motor.stop()
    motor.free()

def endTests():
    debug("Ending tests, freeing motors")
    for i in range(0, 4):
        freeMotor(i)
    cyprus.close()
    
def getFunctionName():
    return eval('sys._getframe({}).f_code.co_name'.format(2))

def getVersion():
    printTitle(cyprus.read_firmware_version())

########################### Test Execution #########################################

initTests()
getVersion()

testSetPWMValues(1)
exit()



cyprus.write_pwm_values(2, period, 0)
print("Done")
sleep(1)



#cyprus.set_motor_speed(2, 0.05)
#pwmAndStepperTest(4, 0)
#gpioInputTest()
#sleep(1)
#cyprus.set_motor_speed(2, 0)
cyprus.close()
exit()

for i in range(0, args.motorCount):
    homeTest(i)
    speedTest(i)
    relativeMoveTest(i, 20)
    encoderTest(i)
    encoderTriggerTest(i, 0x500)
    encoderTriggerAutoResetTest(i, 0x500)
    encoderTriggerRadiusTest(i, 0x50, 0x500)
    freeMotor(i)

if args.motor != -1:
    homeTest(args.motor)
    speedTest(args.motor)
    relativeMoveTest(args.motor, 20)
    readEncoderTest(args.motor)
    encoderTest(args.motor)
    encoderTriggerTest(args.motor, 0x500)
    encoderTriggerAutoResetTest(args.motor, 0x500)
    encoderTriggerRadiusTest(args.motor, 0x50, 0x500)

#pwmSpeedTest(1)
#pwmPositionTest(1)
    
endTests()

