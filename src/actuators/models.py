import actuators.controllers as AC
import time

class Trapdoor(AC.ServoController):
    def __init__(self, gpio_pin, closed_angle, open_angle):
        super().__init__(gpio_pin)  # Initialize the parent class with the gpio_pin
        self.closed_angle = closed_angle
        self.open_angle = open_angle

    def open(self):
        """Sweeps the servo to a high angle to open the trapdoor."""
        print('Trapdoor open')
        self.sweep(self.closed_angle, self.open_angle, 2)

    def close(self):
        """Sweeps the servo to a low angle to close the trapdoor."""
        print('Trapdoor closed')
        self.sweep(self.open_angle, self.closed_angle, 0.5)

class Train(AC.ServoController):
    def __init__(self, gpio_pin, position_A, position_B, position_C):
        super().__init__(gpio_pin)
        self.position_zero = position_A
        self.position_ninety = position_B
        self.position_one_eighty = position_C

    def set_position_zero(self):
        """Sets the train's position to 0 degrees."""
        self.set_angle(self.position_zero)

    def set_position_ninety(self):
        """Sets the train's position to 90 degrees."""
        self.set_angle(self.position_ninety)

    def set_position_one_eighty(self):
        """Sets the train's position to 180 degrees."""
        self.set_angle(self.position_one_eighty)

class SlowMotor(AC.MotorController):
    def __init__(self, gpio_pin, start_velocity, target_velocity, start_duration):
        super().__init__(gpio_pin)
        self.start_velocity = start_velocity
        self.target_velocity = target_velocity
        self.start_duration = start_duration

    def start(self):
        steps = 10
        step_time = self.start_duration / steps
        velocity_step = (self.target_velocity - self.start_velocity) / steps
        
        for i in range(steps):
            velocity = self.start_velocity + i * velocity_step
            self.set_velocity(velocity)
            time.sleep(step_time)
        
        self.set_velocity(self.target_velocity)
