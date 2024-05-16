# Import the pigpio library
import pigpio
import time

pi = None
current_angle = 6

# Initialize the pigpio library
def init():
    global pi

    GPIO_PIN = 13
    PWM_FREQUENCY = 50
    pi = pigpio.pi()

    # Check if pigpio is initialized successfully
    if not pi.connected:
        exit()

    # Set the GPIO pin mode to output
    pi.set_mode(GPIO_PIN, pigpio.OUTPUT)
    pi.set_PWM_frequency(GPIO_PIN, PWM_FREQUENCY)

def set_angle(angle):
    global current_angle

    if (current_angle != angle):
        current_angle = angle

        duty_cycle = angle / 180 * 26 + 6
        print(f"Setting duty cycle: {duty_cycle}")
        pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)

def stop():
    pi.stop()
