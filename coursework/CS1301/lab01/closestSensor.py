import irobot_edu_sdk
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Robot, Root, Create3
print("Successfully installed!")

robot = Create3(Bluetooth("PAIGE"))

@event(robot.when_play)
async def play(robot):
    print("Successfully connected!")

robot.play()

@event(robot.when_play)
async def test(robot):
    await robot.set_lights_on_rgb(0, 255, 0)  # turn lights green
    await robot.wait(2.0)
    await robot.set_lights_on_rgb(255, 0, 0)  # then red
