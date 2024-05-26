import pigpio
import time

gpio_pin = 25
pi = pigpio.pi()

pi.set_mode(gpio_pin, pigpio.OUTPUT)
pi.set_PWM_frequency(gpio_pin, 50)
pi.set_PWM_dutycycle(gpio_pin, 65)


pi.stop()