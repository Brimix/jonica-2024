import actuators.models as models
import constants as const

trapdoor = models.Trapdoor(
    gpio_pin = const.TRAPDOOR_GPIO_PIN,
    closed_angle = const.TRAPDOOR_CLOSED_ANGLE,
    open_angle = const.TRAPDOOR_OPEN_ANGLE
)

train = models.Train(
    gpio_pin = const.TRAIN_GPIO_PIN,
    position_A = const.TRAIN_POSIION_A,
    position_B = const.TRAIN_POSIION_B,
    position_C = const.TRAIN_POSIION_C
)

carrier = models.Carrier(
    gpio_pin = const.CARRIER_GPIO_PIN,
    center_angle = const.CARRIER_CENTER_ANGLE,
    extent = const.CARRIER_EXTENT,
    sweep_duration = const.CARRIER_SWEEP_DURATION,
    wait_time = const.CARRIER_WAIT_TIME
)
