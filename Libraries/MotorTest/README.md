# Motor Testing
Before running the test please ensure that the stepper motor is plugged in correctly to the Slush Board and there is a corresponding limit switch attached and plugged in correctly to the Slush Board

## To test a stepper motor
0. Before running the test you will need a limit switch connected to the associated stepper port
1. Run main.py, it should prompt the user to execute or execute in terminal, you want to execute in terminal.
2. In terminal it will prompt you which port the stepper motor is attached to.
3. It will then ask you if the motor is spinning clockwise, put y for yes and n for no
4. It will then ask this again but if it is counterclockwise
5. If the stepper motor was able to spin clockwise and counterclockwise and stopping upon limit switch press then your stepper is working successfully
