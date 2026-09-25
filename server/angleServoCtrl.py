from time import sleep
import RPi.GPIO as GPIO
import sys

servo_pin = int(sys.argv[1])
angle = int(sys.argv[2])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

duty = angle / 18 + 2.5
pwm.ChangeDutyCycle(duty)
sleep(0.5)
pwm.stop()
GPIO.cleanup()
