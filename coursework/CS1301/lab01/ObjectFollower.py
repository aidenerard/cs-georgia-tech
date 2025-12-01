import irobot_edu_sdk
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("PAIGE-BOT")) # Put robot name here.

@event(robot.when_play)
async def play(robot):
    print("Successfully connected!")
    
# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

STOP = False

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global STOP
    STOP = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)
    

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global STOP
    STOP = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)
    

# --------------------------------------------------------
# Implement followObject() so the robot:
#   - Uses IR proximity readings (4095 / (ir + 1))
#   - Responds to the CENTER sensor:
#         > 15.0 units ---> plate far
#         5.0–15.0 units ---> alignment zone
#         < 5.0 units ---> plate close
#   - In alignment zone, compare sensor 1 and sensor 5
#     (aligned if difference within + or - 25.0)
#   - Include a fail-safe (collision or button press ---> stop)
# --------------------------------------------------------

@event(robot.when_play)
async def followObject(robot):
    global STOP
    while True:
        if STOP:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,0)
            break
        
        distances = (await robot.get_ir_proximity()).sensors
        proximity = [4095 / (ir + 1) for ir in distances]

        center = proximity[3]
        left = proximity[1]
        right = proximity[5]
        
        if center > 15:
            await robot.set_wheel_speeds(5,5)
            await robot.set_lights_rgb(255,255,255)
            await robot.play_note(Note.D7, 0.3)
            
        elif center >= 5 and center <= 15:
            difference = left - right
            if abs(difference) <= 25:
                await robot.set_wheel_speeds(0,0)
                await robot.set_lights_rgb(0,0,255)
                await robot.play_note(Note.D6, 0.3)
            elif difference > 25:
                await robot.set_wheel_speeds(3,-3)
            elif difference < -25:
                await robot.set_wheel_speeds(-3,3)
                
        else:
            await robot.set_wheel_speeds(-5,-5)
            await robot.set_lights_rgb(255,255,0)
            await robot.play_note(Note.D5, 0.3)

        await robot.wait(0.1)
    

# start the robot
robot.play()
