from enum import Enum
from transitions import Machine
import time
import threading
import keyboardWin as keyboard

from actuators.units import train, trapdoor, motor

### States ###
class States(Enum):
    INIT = 'Init'
    RETRIEVING = 'Retrieving'
    CHECK_OBJECT = 'CheckObject'
    ANALYZE_OBJECT = 'AnalyzeObject'
    SELECT_RED_BALL = 'SelectRedBall'
    SELECT_GREEN_BALL = 'SelectGreenBall'
    SELECT_CUBE = 'SelectCube'
    DISPENSE = 'Dispense'

states = [state.value for state in States]

### Transitions ###
transitions = [
    {'trigger': 'start', 'source': States.INIT.value, 'dest': States.RETRIEVING.value},
    {'trigger': 'timeout_retrieve', 'source': States.RETRIEVING.value, 'dest': States.CHECK_OBJECT.value},
    {'trigger': 'object_detected', 'source': States.CHECK_OBJECT.value, 'dest': States.ANALYZE_OBJECT.value},
    {'trigger': 'object_not_detected', 'source': States.CHECK_OBJECT.value, 'dest': States.RETRIEVING.value},

    # Transitions for the different outcomes from the analysis
    {'trigger': 'handle_ball_red', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_RED_BALL.value},
    {'trigger': 'handle_ball_green', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_GREEN_BALL.value},
    {'trigger': 'handle_cube', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_CUBE.value},

    # Timeout transitions for selection states leading to dispensing
    {'trigger': 'timeout_train', 'source': States.SELECT_RED_BALL.value, 'dest': States.DISPENSE.value},
    {'trigger': 'timeout_train', 'source': States.SELECT_GREEN_BALL.value, 'dest': States.DISPENSE.value},
    {'trigger': 'timeout_train', 'source': States.SELECT_CUBE.value, 'dest': States.DISPENSE.value},

    # Final transition to the close state
    {'trigger': 'timeout_dispense', 'source': States.DISPENSE.value, 'dest': States.RETRIEVING.value},
]

### Model ###
class Model(object):
    def start_timer_retrieving(self):
        # Timer set for 5 seconds to transition to CHECK_OBJECT
        timer = threading.Timer(3.0, self.timeout_retrieve, args=[])
        timer.start()
    
    def start_timer_train(self):
        timer = threading.Timer(5.0, self.timeout_train, args=[])
        timer.start()

    def start_timer_dispense(self):
        timer = threading.Timer(4.0, self.timeout_dispense, args=[])
        timer.start()

# Initialize the state machine
model = Model()
machine = Machine(model=model, states=states, transitions=transitions, initial=States.INIT.value, auto_transitions=False)

machine.on_enter_Retrieving('start_timer_retrieving')
machine.on_enter_SelectRedBall('start_timer_train')
machine.on_enter_SelectGreenBall('start_timer_train')
machine.on_enter_SelectCube('start_timer_train')
machine.on_enter_Dispense('start_timer_dispense')

def main():
    global model
    keyboard.init()

    last_state = None   # For debug

    # Mock values
    should_start = False
    is_object = False
    object_color = 'Red'
    object_shape = 'Square'

    try:
        while True:
            ### Debugging bullshit
            key = keyboard.getKey()
            if (key == 's'):
                should_start = True
            if (key == 'w'):
                is_object = not is_object
            if (key == 'c'):
                if (object_color == 'Red'):
                    object_color = 'Green'
                else:
                    object_color = 'Red'
            if (key == 'x'):
                if (object_shape == 'Circle'):
                    object_shape = 'Square'
                else:
                    object_shape = 'Circle'

            if (last_state != model.state):
                print('Entered state ', model.state)
                last_state = model.state
            
            ### Actual code below this point
            if model.state == States.INIT.value:
                # Initialization code here
                train.set_angle(0)
                trapdoor.set_angle(0)
                motor.stop_motor()

                if (should_start):
                    model.start()
                
            elif model.state == States.RETRIEVING.value:
                # - Start motor
                pass
            elif model.state == States.CHECK_OBJECT.value:
                # - Use camera to identify object existance
                time.sleep(2)
                if (is_object):
                    model.object_detected()
                else:
                    model.object_not_detected()
            elif model.state == States.ANALYZE_OBJECT.value:
                # - Stop motor
                # - Use camera to obtain object values
                time.sleep(2)
                if (object_shape == 'Square'):
                    model.handle_cube()
                else:
                    if (object_color == 'Red'):
                        model.handle_ball_red()
                    else:
                        model.handle_ball_green()

                pass
            elif model.state == States.SELECT_RED_BALL.value:
                train.set_position_zero()
                pass
            elif model.state == States.SELECT_GREEN_BALL.value:
                train.set_position_ninety()
                pass
            elif model.state == States.SELECT_CUBE.value:
                train.set_position_one_eighty()
                pass
            elif model.state == States.DISPENSE.value:
                trapdoor.open()
                time.sleep(1)
                trapdoor.close()
                pass
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.stop()

if __name__ == "__main__":
    main()
