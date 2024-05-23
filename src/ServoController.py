import pigpio
import time

class ServoController:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.pi = pigpio.pi()
        self.current_angle = 0
        
        if not self.pi.connected:
            raise Exception("Failed to connect to pigpio daemon")
        
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.gpio_pin, 50)  # 50 Hz for servo control
        self.pi.set_PWM_dutycycle(self.gpio_pin, 100)

    def set_angle(self, angle):
        if self.current_angle != angle:
            self.current_angle = angle
            duty_cycle = angle / 180 * 26 + 6
            self.pi.set_PWM_dutycycle(self.gpio_pin, duty_cycle)

    def sweep(self, angle_start, angle_end, duration):
        step_time = 0.05
        steps = int(duration / step_time)
        duty_step = (angle_end - angle_start) / steps
        
        for i in range(steps):
            angle = angle_start + i * duty_step
            self.set_angle(angle)
            time.sleep(step_time)
        
        self.set_angle(angle_end)

    def stop(self):
        self.pi.stop()
