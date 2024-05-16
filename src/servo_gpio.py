import RPi.GPIO as GPIO
import time

pwm = None

def init():
    global pwm

    # Pin Definitions
    servo_pin = 13  # GPIO pin connected to the servo signal line

    # Setup
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
    GPIO.setup(servo_pin, GPIO.OUT)

    # PWM setup
    pwm_frequency = 50  # Frequency in Hz (20 ms period)
    pwm = GPIO.PWM(servo_pin, pwm_frequency)
    pwm.start(0)

def set_angle(angle):
    global pwm
    # duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle
    duty_cycle = angle
    pwm.ChangeDutyCycle(duty_cycle)

def stop():
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
