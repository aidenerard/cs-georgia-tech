import irobot_edu_sdk
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("PAIGE-BOT"))

@event(robot.when_play)
async def play(robot):
    print("Successfully connected!")
    

CORRECT_CODE = "341124"
current_password = ""

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global current_password
    current_password += "3"
    await robot.play_note(Note.C5, 0.5)
    await checkUserCode(robot)


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global current_password
    current_password += "4"
    await robot.play_note(Note.D5, 0.5)
    await checkUserCode(robot)


# LEFT BUMP
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_left_bumped(robot):
    global current_password
    current_password += "2"
    await robot.play_note(Note.E5, 0.5)
    await checkUserCode(robot)


# RIGHT BUMP
@event(robot.when_bumped, [False, True]) # [left, right]
async def when_right_bumped(robot):
    global current_password
    current_password += "1"
    await robot.play_note(Note.F5, 0.5)
    await checkUserCode(robot)


async def checkUserCode(robot):
    global current_password

    if len(current_password) < len(CORRECT_CODE):
        await robot.set_lights_on_rgb(0, 0, 255)        # blue light for input
        await robot.play_note(Note.C4, 0.3)             # note C4 for input

        if len(current_password) == 1:                  # move forward 
            await robot.set_wheel_speeds(2, 2)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(0, 0)          # stop
        elif len(current_password) == 2:                # move backward 
            await robot.set_wheel_speeds(-2, -2)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(0, 0)          # stop
        elif len(current_password) == 3:                # spin clockwise
            await robot.set_wheel_speeds(5, -5)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(0, 0)          # stop
        elif len(current_password) == 4:                # spin counter-clockwise
            await robot.set_wheel_speeds(-5, 5)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(0, 0)          # stop
        elif len(current_password) == 5:                # move forward faster
            await robot.set_wheel_speeds(-8, 8)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(8, -8)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(0, 0)          # stop
        return
    
    if len(current_password) == len(CORRECT_CODE):
        if current_password == CORRECT_CODE:

            # Green spinning lights
            await robot.set_lights_spin_rgb(0, 255, 0)
            
            # Short happy tune for correct
            await robot.play_note(Note.C4, 0.5)
            await robot.play_note(Note.D4, 0.5)
            await robot.play_note(Note.E4, 0.5)
            await robot.play_note(Note.G4, 0.5)
            await robot.play_note(Note.C5, 0.5)

            # dance
            await robot.set_wheel_speeds(5,5)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(-5,-5)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(10,-10)
            await robot.wait(0.5)
            await robot.set_wheel_speeds(-10,10)
            await robot.wait(8.0)
            await robot.set_wheel_speeds(0,0)
        else:
            current_password = ""
            await robot.set_lights_spin_rgb(255, 0, 0)  # Red blinking lights
            await robot.play_note(Note.A3, 1.0)         # Short sad tune for fail
            await robot.play_note(Note.F3, 0.75)
            await robot.play_note(Note.D3, 0.75)
            await robot.play_note(Note.E3, 1.0)
            await robot.play_note(Note.C3, 1.5)
            await robot.wait(2.0)
            await robot.set_lights_blink_rgb(255,255,255)


@event(robot.when_play)
async def play(robot):
    global current_password
    current_password = ""

    await robot.set_lights_blink_rgb(255, 255, 255)
    await robot.play_note(Note.C4, 0.5)
    await robot.play_note(Note.E4, 0.5)
    await robot.play_note(Note.G4, 0.5)

robot.play()
