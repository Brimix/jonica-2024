from enum import Enum
from transitions import Machine
import time
import threading
import keyboard
import image_processing.process as imp
import computer_vision.functions as cvf

from actuators.units import train, trapdoor, motor

### States ###
class States(Enum):
    INIT = 'Init'
    RETRIEVING = 'Retrieving'
    ANALYZE_OBJECT = 'AnalyzeObject'
    SELECT_RED_BALL = 'SelectRedBall'
    SELECT_GREEN_BALL = 'SelectGreenBall'
    SELECT_CUBE = 'SelectCube'
    DISPENSE = 'Dispense'

states = [state.value for state in States]

### Transitions ###
transitions = [
    {'trigger': 'start', 'source': States.INIT.value, 'dest': States.RETRIEVING.value},
    {'trigger': 'object_detected', 'source': States.RETRIEVING.value, 'dest': States.ANALYZE_OBJECT.value},

    # Transitions for the different outcomes from the analysis
    {'trigger': 'handle_ball_red', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_RED_BALL.value},
    {'trigger': 'handle_ball_green', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_GREEN_BALL.value},
    {'trigger': 'handle_cube', 'source': States.ANALYZE_OBJECT.value, 'dest': States.SELECT_CUBE.value},
    {'trigger': 'handle_none', 'source': States.ANALYZE_OBJECT.value, 'dest': States.RETRIEVING.value},

    # Timeout transitions for selection states leading to dispensing
    {'trigger': 'timeout_train', 'source': States.SELECT_RED_BALL.value, 'dest': States.DISPENSE.value},
    {'trigger': 'timeout_train', 'source': States.SELECT_GREEN_BALL.value, 'dest': States.DISPENSE.value},
    {'trigger': 'timeout_train', 'source': States.SELECT_CUBE.value, 'dest': States.DISPENSE.value},

    # Final transition to the close state
    {'trigger': 'timeout_dispense', 'source': States.DISPENSE.value, 'dest': States.RETRIEVING.value},
]

### Model ###
class Model(object):
    def start_timer_train(self):
        timer = threading.Timer(5.0, self.timeout_train, args=[])
        timer.start()

    def start_timer_dispense(self):
        trapdoor.open()
        timer = threading.Timer(0.1, self.timeout_dispense, args=[])
        timer.start()

    def close_door_dispense(self):
        trapdoor.close()
        motor.start_motor()

    def start_analysis(self):
        self.st = time.time()
    
    def finish_analysis(self):
        span = time.time() - self.st
        print('Analysis duration: ', span)


# Initialize the state machine
model = Model()
machine = Machine(model=model, states=states, transitions=transitions, initial=States.INIT.value, auto_transitions=False)

machine.on_enter_SelectRedBall('start_timer_train')
machine.on_enter_SelectGreenBall('start_timer_train')
machine.on_enter_SelectCube('start_timer_train')
machine.on_enter_Dispense('start_timer_dispense')
machine.on_exit_Dispense('close_door_dispense')
machine.on_enter_AnalyzeObject('start_analysis')
machine.on_exit_AnalyzeObject('finish_analysis')

def main():
    global model
    keyboard.init()
    imp.init()

    last_state = None   # For debug

    # Mock values
    should_start = False

    try:
        while True:
            ### Debugging bullshit
            key = keyboard.getKey()
            if (key == 's'):
                should_start = True

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
                    motor.start_motor()
                    model.start()
                
            elif model.state == States.RETRIEVING.value:
                is_object = cvf.identify_object()
                if (is_object):
                    model.object_detected()
            elif model.state == States.ANALYZE_OBJECT.value:
                motor.stop_motor()
                
                obj = cvf.get_mode_object()
                if (obj is not None):
                    color, shape = obj

                    if (shape == 'square'):
                        model.handle_cube()
                    else:
                        if (color == 'red'):
                            model.handle_ball_red()
                        else:
                            model.handle_ball_green()
                else:
                    model.handle_none()

            elif model.state == States.SELECT_RED_BALL.value:
                train.set_position_zero()
            elif model.state == States.SELECT_GREEN_BALL.value:
                train.set_position_ninety()
            elif model.state == States.SELECT_CUBE.value:
                train.set_position_one_eighty()
            elif model.state == States.DISPENSE.value:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.stop()
        motor.stop_motor()

if __name__ == "__main__":
    main()
