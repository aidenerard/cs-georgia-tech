from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("DANNY-BOT"))  # Will connect to the first robot found.

HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
SENSOR2CHECK = 0
HAS_ARRIVED = False
DESTINATION = (0, 100)
ARRIVAL_THRESHOLD = 5.0
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
HEADING = 90

STOP = False

# Implementation for fail-safe robots
# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global STOP
    STOP = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)
    return

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global STOP
    STOP = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)
    return

# ==========================================================

# Helper Functions
def getMinProxApproachAngle(readings):
    global STOP
    if STOP:
        return (0,0)
    
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

    proximities = []
    for r in readings:
        proximity  = 4095/(r + 1)
        proximities.append(proximity)

    max_index = 0
    max_value = proximities[0]

    for i, value in enumerate(proximities):
        if value < max_value:
            max_value = value
            max_index = i

    closestDistance = round(max_value, 3)
    closestAngle = IR_ANGLES[max_index]

    return(closestDistance, closestAngle)

def getCorrectionAngle(heading):
    global STOP
    if STOP:
        return 0

    correctionAngle = heading - 90
    correctionAngle = int(correctionAngle)

    return correctionAngle

def getAngleToDestination(currentPosition, destination):
    global STOP
    if STOP:
        return 0
    dx = destination[0] - currentPosition[0]
    dy = destination[1] - currentPosition[1]

    angle_radians = m.atan2(dx,dy)
    angle_degrees = m.degrees(angle_radians)
    
    angleToDestination = int(angle_degrees)
    return angleToDestination

def checkPositionArrived(currentPosition, destination, threshold):
    global STOP
    if STOP:
        return
    
    dx = destination[0] - currentPosition[0]
    dy = destination[1] - currentPosition[1]
    totalDistance = m.sqrt((dx)**2 + (dy)**2)
    print(totalDistance)
    if totalDistance <= threshold:
        return True
    else:
        print(2)
        return False

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    global STOP
    if STOP:
        return
    
    pose = await robot.get_position()
    currentX = pose.x
    currentY = pose.y
    heading = pose.heading
    print(heading)

    angleToDestination = getAngleToDestination((currentX, currentY), DESTINATION)
    print(f"Destination Angle: {angleToDestination}")
    correctionAngle = getCorrectionAngle(heading)
    print(f"Correction Angle: {correctionAngle}")

    #turnAngle = correctionAngle - angleToDestination
   
    await robot.turn_right(correctionAngle)
    await robot.turn_right(angleToDestination)

# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global STOP, SENSOR2CHECK
    if STOP:
        return

    await robot.set_wheel_speeds(15,15)

    while not STOP:
        readings = (await robot.get_ir_proximity()).sensors

        closestDistance, closestAngle = getMinProxApproachAngle(readings)

        if closestDistance < 20:
            HAS_FOUND_OBSTACLE = True
            await robot.set_wheel_speeds(0, 0)

            if closestAngle < 0:
                turnAngle = closestAngle + 90
            else:
                turnAngle = closestAngle - 90
                
            await robot.turn_right(turnAngle)

            SENSOR2CHECK = readings.index(min(readings))
    
            await followObstacle(robot)
            HAS_FOUND_OBSTACLE = False
            HAS_REALIGNED = False
            break

        await robot.wait(0.1)

# === FOLLOW OBSTACLE
async def followObstacle(robot):
    global STOP, SENSOR2CHECK
    if STOP:
        return
    
    await robot.set_wheel_speeds(15,15)

    while not STOP:
        readings = (await robot.get_ir_proximity()).sensors
        proximity = 4095 / (readings[SENSOR2CHECK] + 1)

        closestDistance, closestAngle = getMinProxApproachAngle(readings)
        if proximity < 20:
            await robot.set_wheel_speeds(0,0)

            if closestAngle > 0:
                await robot.turn_right(-3)
            else:
                await robot.turn_right(3)
            await robot.set_wheel_speeds(15,15)

        elif proximity > 100:
            await robot.set_wheel_speeds(15,15)
            await robot.wait(1.5)
            await robot.set_wheel_speeds(0,0)
            await realignRobot(robot)
            break

        else:
            await robot.set_wheel_speeds(15,15)

        await robot.wait(0.1)      

# ==========================================================

# Main function
import csv
@event(robot.when_play)
async def makeDelivery(robot):
    global STOP, HAS_COLLIDED, HAS_REALIGNED, HAS_FOUND_OBSTACLE, SENSOR2CHECK, HAS_ARRIVED, DESTINATION, ARRIVAL_THRESHOLD
    
    await robot.set_lights_rgb(0,0,255)
    await robot.set_wheel_speeds(0,0)

    while not HAS_ARRIVED and not STOP:
        pose = await robot.get_position()
        currentX = pose.x
        currentY = pose.y

        with open("PositionData.csv", "a") as f:
            write = csv.writer(f)
            write.writerow([pose.x, pose.y])
        
        heading = pose.heading
        print(f"Heading: {heading}")
        print(f"X: {currentX}")
        print(f"Y: {currentY}")

        if checkPositionArrived((currentX, currentY), DESTINATION, ARRIVAL_THRESHOLD):
            print("ARRIVED!")
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_spin_rgb(0,255,0)
            await robot.set_wheel_speeds(0,15)
            await robot.wait(4)
            HAS_ARRIVED = True
            break

        if not HAS_REALIGNED:
            await realignRobot(robot)
            HAS_REALIGNED = True

        await moveTowardGoal(robot)

        if HAS_FOUND_OBSTACLE:
            await followObstacle(robot)
            HAS_FOUND_OBSTACLE = False
            HAS_REALIGNED = False

        await robot.wait(0.1)

    await robot.set_wheel_speeds(0,0)
    return

# start the robot
robot.play()
