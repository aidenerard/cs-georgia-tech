import math as m

STOP = False

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
    
    if heading > 90:
        correctionAngle = -(90 - heading)
    elif heading <= 90:
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

    if totalDistance <= threshold:
        return True
    else:
        return False
