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

class Carrier(AC.ServoController):
    def __init__(self, gpio_pin, center_angle, extent, sweep_duration, wait_time):
        super().__init__(gpio_pin)
        self.center_angle = center_angle
        self.extent = extent
        self.sweep_duration = sweep_duration
        self.wait_time = wait_time

    def operate(self):
        """
        Operates the carrier by sweeping from the center to half the extent in one direction,
        waits, then sweeps to the full extent in the opposite direction, waits, and returns to center.
        """
        # Calculate the target positions based on the center and extent
        left_target = self.center_angle - self.extent / 2
        right_target = self.center_angle + self.extent / 2

        # Sweep to the left target
        self.sweep(self.center_angle, left_target, self.sweep_duration)
        time.sleep(self.wait_time)

        # Sweep to the right target
        self.sweep(left_target, right_target, self.sweep_duration * 2)
        time.sleep(self.wait_time)

        # Return to the center
        self.sweep(right_target, self.center_angle, self.sweep_duration)
