from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("BAYMAX"))   # Put robot name here.

# IR Sensor Angles
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

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
# Implement robotPong() so that the robot:
#     Sets the initial light to cyan.
#     Moves in a straight line at 15 units/s.
#     CONTINUOUSLY checks IR readings for nearby walls.
#     If the closest wall is <= 20 units away,
#         Momentarily stop.
#         Reflect its direction based on the angle of the wall.
#         Change the light from cyan to magenta, or vice versa.
# --------------------------------------------------------

@event(robot.when_play)
async def robotPong(robot):

    global STOP
    """
    Use the following two lines somewhere in your code to calculate the
    angle and direction of reflection from a list of IR readings:
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)
        (direction, turningAngle) = calculateReflectionAngle(approx_angle)
    Then, if the closest wall is less than 20 cm away, use the
    direction and the turningAngle to determine how to rotate the robot to
    reflect.
    """

    await robot.set_lights_rgb(0,255,255)
    await robot.set_wheel_speeds(15,15)

    color_is_cyan = True

    while not STOP:
        
        ir_readings = (await robot.get_ir_proximity()).sensors
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)
        (direction, turningAngle) = calculateReflectionAngle(approx_angle)

        if approx_dist <= 20:
            await robot.set_wheel_speeds(0,0)

            if color_is_cyan:
                await robot.set_lights_rgb(255,0,255)
            else:
                await robot.set_lights_rgb(0,255,255)
            color_is_cyan = not color_is_cyan
        
            if direction == "right":
                await robot.turn_right(turningAngle)
            else:
                await robot.turn_left(turningAngle)

            await robot.wait(0.5)
            await robot.set_wheel_speeds(15,15)

    await robot.set_wheel_speeds(0,0)

def angleOfClosestWall(readings):
    """Remember that this function can be autograded!"""
    # determine which sensor detects the closest wall
    # return the proximity and corresponding sesnor angle
    # Arguments -> readings(list): 7 IR sensor readings
    # Returns   -> tuple: (closestDistance, closestAngle)
    
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

    proximities = []
    for r in readings:
        proximity  = 4095/(r + 1)
        proximities.append(proximity)

    min_index = 0
    min_value = proximities[0]

    for i, value in enumerate(proximities):
        if value < min_value:
            min_value = value
            min_index = i

    closestDistance = round(min_value, 3)
    closestAngle = IR_ANGLES[min_index]

    return(closestDistance, closestAngle)

def calculateReflectionAngle(angle):
    """Remember that this function can be autograded!"""
    if angle < 0:
        direction = "right"
        turningAngle = 180 + 2 * angle
    else:
        direction = "left"
        turningAngle = 180 - 2 * angle

    turningAngle = round(turningAngle, 3)
    return(direction, turningAngle)

# start the robot
robot.play()
