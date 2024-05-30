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
        self.pi.set_PWM_dutycycle(self.gpio_pin, 0)

    def set_angle(self, angle):
        if self.current_angle != angle:
            self.current_angle = angle
            duty_cycle = angle / 180 * 26 + 6
            self.pi.set_PWM_dutycycle(self.gpio_pin, duty_cycle)

    def sweep(self, start_angle, target_angle, duration):
        step_time = 0.05
        steps = int(duration / step_time)
        duty_step = (target_angle - start_angle) / steps
        
        for i in range(steps):
            angle = start_angle + i * duty_step
            self.set_angle(angle)
            time.sleep(step_time)
        
        self.set_angle(target_angle)

    def sweep_to(self, target_angle, duration):
        """
        Sweeps the servo from the current angle to the target angle over the specified duration.
        
        :param target_angle: The angle to sweep to.
        :param duration: The time over which to perform the sweep.
        """
        self.sweep(self.current_angle, target_angle, duration)

    def stop(self):
        self.pi.stop()
