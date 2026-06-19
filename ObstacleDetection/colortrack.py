from pybricks.hubs import PrimeHub
from pybricks.messaging import AppData
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from ustruct import unpack


hub = PrimeHub()

steering = Motor(Port.D, Direction.CLOCKWISE)
steering.reset_angle(0)

# 8 bytes: rx, ry, rw, rh, gx, gy, gw, gh
app = AppData([(0, 8)])
app.configure(0, 0, bytes([0]))


def clamp(v):
    if v > 45:
        return 45
    if v < -45:
        return -45
    return v


def seen(w):
    return w > 2   # filter noise



while True:

    data = app.get_bytes(0)

    if data:
        rx, ry, rw, rh, gx, gy, gw, gh = unpack("BBBBBBBB", data)
    else:
        rx = ry = rw = rh = 0
        gx = gy = gw = gh = 0

    red_seen = seen(rw)
    green_seen = seen(gw)

    if red_seen or green_seen:

        # choose closest (bigger width = closer)
        if red_seen and green_seen:

            if rw >= gw:
                active = "red"
                x = rx
                strength = rw
            else:
                active = "green"
                x = gx
                strength = gw

        elif red_seen:
            active = "red"
            x = rx
            strength = rw

        else:
            active = "green"
            x = gx
            strength = gw

    else:
        steering.run_target(300, 0, wait=False)
        wait(20)
        continue

    # ---------------- STEERING ----------------

    error = x - 30

    steering_angle = error * 2

    steering_angle *= (strength / 10)

    steering_angle = clamp(steering_angle)

    steering.run_target(300, steering_angle, wait=False)

    wait(20)