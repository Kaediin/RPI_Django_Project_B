import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

def activate_schuifregister():
    while True:
        for y in range(8):
            GPIO.output(13, 1)
            controlLeds()

        for y in range(8):
            GPIO.output(13, 0)
            controlLeds()

def controlLeds():
    time.sleep(0.1)
    GPIO.output(5, 1)
    time.sleep(0.1)
    GPIO.output(5, 0)
    GPIO.output(13, 0)
    GPIO.output(6, 1)
    time.sleep(0.1)
    GPIO.output(6, 0)
