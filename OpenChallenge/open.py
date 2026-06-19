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
right_sensor = UltrasonicSensor(Port.C)

#SETTINGS


KP = 2.25
KD = 0.1
MAX_STEER = 40

TURN_ANGLE = 90

#STATE
Speed = 175
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
    for i in range(20):
        total += sensor.distance()
        wait(7)
    return total / 20

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

    drive.drive(Speed, 0)

def drive_straight_cm(distance_cm, speed=300):
    global target_heading, last_error

    # resetiraj encoder (koliko su kotači prošli)
    drive.reset()
    
    start_heading = target_heading

    target_mm = distance_cm * 10  # cm → mm

    while drive.distance() < target_mm:

        heading = hub.imu.heading()

        error = normalize(start_heading - heading)
        derivative = error - last_error

        steer = KP * error + KD * derivative
        steer = clamp(steer, -MAX_STEER, MAX_STEER)

        steering.run_target(500, steer, wait=False)

        drive.drive(speed, 0)

        last_error = error
        wait(10)

    drive.stop()

#TURNS

def turn_left_90():
    global target_heading, last_error

    print("TURN LEFT 90")

    start = hub.imu.heading()
    target = start - TURN_ANGLE

    target_heading -= TURN_ANGLE

    steering.run_target(300, -40, wait=False)
    drive.drive(75, 0)

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
    drive.drive(75, 0)

    while hub.imu.heading() < (target - 2):
        wait(5)

    steering.run_target(300, 0, wait=True)

    last_error = 0
    wait(150)


#INIT

hub.imu.reset_heading(0)
wait(300)

drive.drive(Speed, 0)

#MAIN
left_Active = True
right_Active = True
count = 0

print("L", left_sensor.distance(), "R", right_sensor.distance())
wait(600)
while count < 12:

    left_dist = filtered_distance(left_sensor)
    right_dist = filtered_distance(right_sensor)

    event = False

    # LEFT
    if left_Active and left_dist > 1999:
        right_Active = False
        turn_left_90()

        while filtered_distance(left_sensor) > 1700:
            gyro_follow()
            wait(10)

        event = True

    # RIGHT
    elif right_Active and right_dist > 1999:
        left_Active = False
        turn_right_90()

        while filtered_distance(right_sensor) > 1700:
            gyro_follow()
            wait(10)

        event = True
    Speed = 175
    gyro_follow()
    wait(10)

    # COUNT samo ako se stvarno nešto dogodilo
    if event:
        count += 1

print("Gotov")
steering.run_target(300, 0, wait=True)
