from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
import math as m

# robot setup
robot = Create3(Bluetooth("HRISTO-BOT"))  # change to your robot name

HAS_COLLIDED = False
SENSOR2CHECK = 0       # 0 = left wall, 6 = right wall
ARRIVAL_THRESHOLD = 10 # how close to gap center to stop

# ==== fail-safes ====

@event(robot.when_touched, [True, True])
async def when_either_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)

@event(robot.when_bumped, [True, True])
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)

# ==== small heading correction ====

async def courseCorrect(robot, target_heading=90.0):
    """Turn slightly to keep heading near target_heading."""
    global HAS_COLLIDED
    if HAS_COLLIDED:
        return

    pose = await robot.get_position()
    heading = pose.heading % 360

    error = (heading - target_heading + 180) % 360 - 180

    if error > 3:
        await robot.turn_right(min(error, 5))
    elif error < -3:
        await robot.turn_left(min(-error, 5))

# ==== findWall: pick which side to track ====

async def findWall(robot):
    global HAS_COLLIDED, SENSOR2CHECK
    HAS_COLLIDED = False

    await robot.set_lights_rgb(0, 0, 255)
    await robot.set_wheel_speeds(5, 5)

    while not HAS_COLLIDED:
        sensors = (await robot.get_ir_proximity()).sensors
        left_dist = 4095 / (sensors[0] + 1)
        right_dist = 4095 / (sensors[6] + 1)

        if left_dist < 60 or right_dist < 60:
            await robot.set_wheel_speeds(0, 0)

            if left_dist < right_dist:
                SENSOR2CHECK = 0
            else:
                SENSOR2CHECK = 6

            await robot.set_lights_rgb(0, 255, 255)
            break

        await courseCorrect(robot, target_heading=90.0)
        await robot.wait(0.1)

    await robot.set_wheel_speeds(0, 0)

# ==== calculateGap: start/end of a single gap ====

async def calculateGap(robot):
    global SENSOR2CHECK, HAS_COLLIDED
    if HAS_COLLIDED:
        return ((0, 0), (0, 0))

    pose = await robot.get_position()
    start_pos = (pose.x, pose.y)

    await robot.set_wheel_speeds(5, 5)

    while not HAS_COLLIDED:
        await courseCorrect(robot, target_heading=90.0)

        sensors = (await robot.get_ir_proximity()).sensors
        side_dist = 4095 / (sensors[SENSOR2CHECK] + 1)

        if side_dist < 60:
            await robot.set_wheel_speeds(0, 0)
            break

        await robot.wait(0.1)

    pose = await robot.get_position()
    end_pos = (pose.x, pose.y)

    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    gap_len = m.sqrt(dx * dx + dy * dy)

    return (start_pos, end_pos)

# ==== findGaps: scan along wall and pick largest ====

async def findGaps(robot):
    global SENSOR2CHECK, HAS_COLLIDED
    gaps = []

    await robot.set_lights_rgb(0, 255, 255)
    await robot.set_wheel_speeds(5, 5)

    while not HAS_COLLIDED:
        sensors = (await robot.get_ir_proximity()).sensors

        # stop scan when front wall within ~10 units
        front_dist = 4095 / (sensors[3] + 1)
        if front_dist < 10:
            await robot.set_wheel_speeds(0, 0)
            break

        side_dist = 4095 / (sensors[SENSOR2CHECK] + 1)

        # gap: side opens up (bigger distance value)
        if side_dist > 200:
            gap = await calculateGap(robot)
            gaps.append(gap)
            await robot.set_wheel_speeds(5, 5)

        await courseCorrect(robot, target_heading=90.0)
        await robot.wait(0.1)

    if not gaps:
        return ((0, 0), (0, 0))

    largest_gap = None
    largest_len = -1.0
    for i, gap in enumerate(gaps):
        (x1, y1) = gap[0]
        (x2, y2) = gap[1]
        dist = m.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if dist > largest_len:
            largest_len = dist
            largest_gap = gap

    return largest_gap

# ==== park: go to center of largest gap, then enter ====

async def park(robot):
    global SENSOR2CHECK, HAS_COLLIDED

    largest_gap = await findGaps(robot)
    if HAS_COLLIDED:
        return

    (x1, y1) = largest_gap[0]
    (x2, y2) = largest_gap[1]

    gap_size = m.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    if gap_size < 50:  
        await robot.set_lights_rgb(255, 0, 0)
        await robot.set_wheel_speeds(0, 0)
        return

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    pose = await robot.get_position()
    curr_x, curr_y = pose.x, pose.y

    dx = center_x - curr_x
    dy = center_y - curr_y

    angle_to_center = m.degrees(m.atan2(dy, dx))
    current_heading = pose.heading

    turn_angle = angle_to_center - current_heading
    if turn_angle > 180:
        turn_angle -= 360
    elif turn_angle < -180:
        turn_angle += 360

    if turn_angle > 0:
        await robot.turn_right(turn_angle)
    else:
        await robot.turn_left(-turn_angle)

    drive_heading = angle_to_center
    await robot.set_wheel_speeds(5, 5)

    while not HAS_COLLIDED:
        pose = await robot.get_position()
        curr_x, curr_y = pose.x, pose.y

        dist_to_center = m.sqrt((center_x - curr_x)**2 + (center_y - curr_y)**2)

        if dist_to_center <= ARRIVAL_THRESHOLD:
            break

        await courseCorrect(robot, target_heading=drive_heading)
        await robot.wait(0.1)

    await robot.set_wheel_speeds(0, 0)

    if HAS_COLLIDED:
        return

    if SENSOR2CHECK == 0:
        await robot.turn_right(90)
    else:
        await robot.turn_left(90)

    await robot.move(45)

    await robot.set_lights_spin_rgb(0, 255, 0)
    await robot.play_note(Note.A5, 0.5)
    await robot.wait(0.5)
    await robot.play_note(Note.C6, 0.5)

# ==== main ====

@event(robot.when_play)
async def selfParking(robot):
    global HAS_COLLIDED

    HAS_COLLIDED = False
    await findWall(robot)

    if not HAS_COLLIDED:
        await park(robot)

    await robot.set_wheel_speeds(0, 0)

robot.play()
