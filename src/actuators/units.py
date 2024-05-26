import actuators.models as models

trapdoor = models.Trapdoor(gpio_pin=12)
train = models.Train(gpio_pin=13)

motor = models.Motor(gpio_pin=25) 