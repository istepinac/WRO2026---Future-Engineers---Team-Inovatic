from gpiozero import DistanceSensor
from time import sleep

left_sensor = DistanceSensor(echo=24, trigger=23)

while True:
    print(left_sensor.distance * 100)
    sleep(0.1)