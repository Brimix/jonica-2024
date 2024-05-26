import actuators.controllers as AC

class Trapdoor(AC.ServoController):
    def open(self):
        """Sweeps the servo from 0 to 90 degrees to open the trapdoor."""
        print('Trapdoor open')
        self.sweep(0, 90, 2)

    def close(self):
        """Sweeps the servo from 90 to 0 degrees to close the trapdoor."""
        print('Trapdoor closed')
        self.sweep(90, 0, 0.5)

class Train(AC.ServoController):
    def set_position_zero(self):
        """Sets the train's position to 0 degrees."""
        # print('Train to 0')
        self.set_angle(1)

    def set_position_ninety(self):
        """Sets the train's position to 90 degrees."""
        self.set_angle(90)

    def set_position_one_eighty(self):
        """Sets the train's position to 180 degrees."""
        self.set_angle(179)

class Motor(AC.MotorController):
    pass