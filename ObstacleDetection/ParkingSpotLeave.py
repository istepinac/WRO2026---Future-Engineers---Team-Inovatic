from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

# ---------------- MOTORI ----------------

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

# ---------------- SENSORS -----------------

left_sensor = UltrasonicSensor(Port.E)
right_sensor = UltrasonicSensor(Port.C)

# ---------------- SETTINGS ----------------


KP = 2.0
KD = 0.5
MAX_STEER = 40

TURN_ANGLE = 90
THRESHOLD = 250  # 25 cm

# ---------------- STATE ----------------

target_heading = 0
last_error = 0

left_blocked = False
right_blocked = False

startup_done = False

# ---------------- HELPERS ----------------

def clamp(v, mn, mx):
    return max(mn, min(mx, v))

def normalize(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

# ---------------- STARTUP ROUTINE ----------------

def startup_routine():
    global startup_done

    if startup_done:
        return
    startup_done = True

    print("STARTUP ROUTINE")

    if right_sensor.distance() > left_sensor.distance():
        left_blocked = True
        drive.straight(-25)
        steering.run_target(300, 40, wait=False)
        wait(100)
        for i in range(4):
            drive.straight(50)
            steering.run_target(300, -40, wait=False)
            wait(100)

            drive.straight(-60)
            steering.run_target(300, 40, wait=False)
            wait(100)


        drive.straight(50)
        steering.run_target(300, -40, wait=False)
        wait(100)

        steering.run_target(300, 0, wait=False)
        drive.straight(200)
        steering.run_target(300, -40, wait=False)
        drive.drive(150,0)
        print("1")
        while hub.imu.heading() > 0:
            print("2")
            wait(5)
        steering.run_target(300, 0, wait=False)
        drive.stop()
        wait(200)

    else:
        right_blocked = True
        drive.straight(-25)
        steering.run_target(300, -40, wait=False)
        wait(100)
        for i in range(4):

            drive.straight(50)
            steering.run_target(300, 40, wait=False)
            wait(100)

            drive.straight(-60)
            steering.run_target(300, -40, wait=False)
            wait(100)


        drive.straight(50)
        steering.run_target(300, 40, wait=False)
        wait(100)

        steering.run_target(300, 0, wait=False)

        drive.straight(200)

        steering.run_target(300, 40, wait=False)
        drive.drive(150,0)
        print("1")
        while hub.imu.heading() < 0:
            print("2")
            wait(5)
        steering.run_target(300, 0, wait=False)
        print(3)
        drive.stop()
        wait(200)

    wait(200)

# ---------------- PID DRIVE ----------------

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

# ---------------- TURN LEFT ----------------

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

# ---------------- TURN RIGHT ----------------

def turn_right_90():
    global target_heading, last_error

    print("TURN RIGHT 90")

    start = hub.imu.heading()
    target = start + TURN_ANGLE
    target_heading += TURN_ANGLE

    steering.run_target(300, 40, wait=False)
    drive.drive(75, 0)

    while hub.imu.heading() < target:
        wait(5)

    steering.run_target(300, 0, wait=True)

    last_error = 0
    wait(150)

# ---------------- INIT ----------------
Speed = 175
hub.imu.reset_heading(0)
target_heading = 0
last_error = 0

startup_routine()

drive.drive(175, 0)

# ---------------- MAIN LOOP ----------------

while True:
    if not left_blocked and left_sensor.distance() > 1500:
        wait(100)
        turn_left_90()

        while left_sensor.distance() > 1700:
            gyro_follow()
            wait(10)

    if not right_blocked and right_sensor.distance() > 1500:
        wait(100)
        turn_right_90()

        while right_sensor.distance() > 1700:
            gyro_follow()
            wait(10)

    Speed = 175
    gyro_follow()
    wait(10)