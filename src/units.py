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

motor = models.SlowMotor(
    gpio_pin = const.MOTOR_GPIO_PIN,
    start_velocity = const.MOTOR_HIGH_PWM,
    target_velocity = const.MOTOR_SLOW_PWM,
    start_duration = const.MOTOR_START_DURATION
)
