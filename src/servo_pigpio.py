# Import the pigpio library
import pigpio
import time

pi = None
current_angle = 0

GPIO_PIN = 13

# Initialize the pigpio library
def init():
    global pi, GPIO_PIN

    PWM_FREQUENCY = 50
    pi = pigpio.pi()

    # Check if pigpio is initialized successfully
    if not pi.connected:
        exit()

    # Set the GPIO pin mode to output
    pi.set_mode(GPIO_PIN, pigpio.OUTPUT)
    pi.set_PWM_frequency(GPIO_PIN, PWM_FREQUENCY)

def set_angle(angle):
    global current_angle, GPIO_PIN

    if (current_angle != angle):
        current_angle = angle

        duty_cycle = angle / 180 * 26 + 6
        # print(f"Setting duty cycle: {duty_cycle}")
        pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)

def sweep(angle_start, angle_end, duration):
    step_time = 0.02
    steps = int(duration / step_time)
    duty_step = (angle_end - angle_start) / steps
    
    for i in range(steps):
        angle = angle_start + i * duty_step
        set_angle(angle)
        time.sleep(step_time)
    
    set_angle(angle_end) 

def stop():
    pi.stop()
