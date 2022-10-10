#!/usr/bin/python3
import re
import sys
try:
    from pidev.stepper import stepper
except (ImportError, ModuleNotFoundError):
    sys.exit("Stepper libraries (pidev/slush) were not found. Install slushengine or pidev from RaspberryPiCommon")


def run_stepper(stepper):
    stepper.run(1, 2500)
    print("Motor should be spinning clockwise until the limit switch on port %s is pressed" % user_input_port)
    while stepper.read_switch() == 0:
        continue

    check_if_spinning(True)

    stepper.run(0, 2500)
    print("Motor should be spinning counterclockwise until the limit switch on port %s is pressed" % user_input_port)
    while stepper.read_switch() == 0:
        continue

    check_if_spinning(False)

    stepper.hardStop()
    stepper.free()


def check_if_spinning(clockwise):
    if clockwise:
        clock_wise_user_prompt = input("Was the motor spinning clockwise? [y/n]\n")

        try:
            if clock_wise_user_prompt == "y":
                return
            elif clock_wise_user_prompt == "n":
                print("The motor test has failed, the motor should have been spinning clockwise")
                test_stepper.free()
                input("Press any key to exit")
                sys.exit()
            else:
                raise ValueError("Not a valid response\n")
        except ValueError as error:
            print(error)
            input("Was the motor spinning clockwise? [y/n]\n")

    else:
        counter_clock_wise_user_prompt = input("Was the motor spinning counter clockwise? [y/n]\n")

        try:
            if counter_clock_wise_user_prompt == "y":
                return
            elif counter_clock_wise_user_prompt == "n":
                print("The motor test has failed, the motor should have been spinning counterclockwise")
                test_stepper.free()
                input("Press any key to exit")
                sys.exit()
            else:
                raise ValueError("Not a valid response\n")
        except ValueError as error:
            print(error)
            input("Was the motor spinning clockwise? [y/n]\n")


def check_user_input_port(user_input_port):
    regex = r"[0123]"
    matches = re.finditer(regex, user_input_port)

    for match_num, match in enumerate(matches):
        match_num = match_num + 1

        return match_num


if __name__ == "__main__":
    input("You will need a limit switch before running this test, press any key when you are ready\n")
    user_input_port = input("Which port is the stepper attached to?\n")

    valid_user_input = False
    test_stepper = None

    while not valid_user_input:
        try:
            if int(check_user_input_port(user_input_port)) >= 1:
                int(user_input_port)
                valid_user_input = True

            else:
                raise ValueError("Not a valid response")
        except ValueError as error:
            print(error)
            user_input_port = input("Which port is the stepper attached to?\n")
    try:
        test_stepper = stepper(port=int(user_input_port))
        run_stepper(test_stepper)
    except KeyboardInterrupt:
        test_stepper.free()
        sys.exit("Exiting")

    test_stepper.free()
    print("Congratulations, the motor test was successful")
    input("\nPress any key to exit")
