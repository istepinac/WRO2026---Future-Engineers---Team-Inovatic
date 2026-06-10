from gpiozero import Servo, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

factory = PiGPIOFactory()

steering = Servo(18, pin_factory=factory)

left_sensor = DistanceSensor(echo=20, trigger=21, pin_factory=factory)
right_sensor = DistanceSensor(echo=27, trigger=17, pin_factory=factory)

Kp = 0.05
DEADZONE = 5

def steer(value):
    sleep(0.2)
    steering.value = value

try:
    while True:
        GPIO.output(24, GPIO.HIGH)
        left = left_sensor.distance * 100
        right = right_sensor.distance * 100

        error = left - right

        if abs(error) < DEADZONE:
            error = 0

        steering_value = error * Kp
        steering_value = max(min(steering_value, 1), -1)

        steer(steering_value)

        print("L:", left, "R:", right, "ERR:", error, "STEER:", steering_value)

        sleep(0.05)

except KeyboardInterrupt:
    print("\nProgram prekinut.")

finally:
    GPIO.output(24, GPIO.LOW)  
    GPIO.cleanup()
    steer(0.22)
    print("GPIO24 ugašen.")