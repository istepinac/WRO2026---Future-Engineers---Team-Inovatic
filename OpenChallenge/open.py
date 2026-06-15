from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

#MOTORS

left_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, Direction.CLOCKWISE)

drive = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=56,
    axle_track=114
)

steering = Motor(Port.D)
steering.reset_angle(0)

#SENSORS

left_sensor = UltrasonicSensor(Port.E)
right_sensor = UltrasonicSensor(Port.A)

#SETTINGS

SPEED = 340

KP = 4.0
KD = 0.5
MAX_STEER = 40

TURN_ANGLE = 90

#STATE

target_heading = 0
last_error = 0

#HELPERS

def clamp(v, mn, mx):
    return max(mn, min(mx, v))

def normalize(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle



def filtered_distance(sensor):
    total = 0
    for i in range(5):
        total += sensor.distance()
        wait(3)
    return total / 5


#PID DRIVE

def gyro_follow():
    global last_error

    heading = hub.imu.heading()

    error = normalize(target_heading - heading)
    derivative = error - last_error

    steer = KP * error + KD * derivative
    steer = clamp(steer, -MAX_STEER, MAX_STEER)

    steering.run_target(500, steer, wait=False)

    last_error = error

    drive.drive(SPEED, 0)


#TURNS

def turn_left_90():
    global target_heading, last_error

    print("TURN LEFT 90")

    start = hub.imu.heading()
    target = start - TURN_ANGLE

    target_heading -= TURN_ANGLE

    steering.run_target(300, -40, wait=False)
    drive.drive(SPEED, 0)

    while hub.imu.heading() > target:
        wait(5)

    steering.run_target(300, 0, wait=True)

    last_error = 0
    wait(150)


def turn_right_90():
    global target_heading, last_error

    print("TURN RIGHT 90")

    start = hub.imu.heading()
    target = start + TURN_ANGLE

    target_heading += TURN_ANGLE

    steering.run_target(300, 40, wait=False)
    drive.drive(SPEED, 0)

    while hub.imu.heading() > target:
        wait(5)

    steering.run_target(300, 0, wait=True)

    last_error = 0
    wait(150)


#INIT

hub.imu.reset_heading(0)
wait(300)

drive.drive(SPEED, 0)

#MAIN

while True:

    left_dist = filtered_distance(left_sensor)
    right_dist = filtered_distance(right_sensor)


    if filtered_distance(left_sensor) > 1500:
        wait(100)
        turn_left_90()

        while filtered_distance(left_sensor) > 1500:
            gyro_follow()
            wait(10)


    if filtered_distance(right_sensor) > 1500:
        wait(100)
        turn_right_90()

        while filtered_distance(right_sensor) > 1500:
            gyro_follow()
            wait(10)

    gyro_follow()
    wait(10)