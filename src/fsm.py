from transitions import Machine
import keyboard
import time
import parameters as param

class Model(object):
    pass

# States
states = [
    'Init',
    'Retreiving',
    'CheckObject',
    'AnalyzeObject',
    'SelectRedBall', 'SelectGreenBall', 'SelectCube',
    'Dispense',
    'Close'
]

# Define the transitions
transitions = [
    {'trigger': 'start', 'source': 'Init', 'dest': 'Retreiving'},
    {'trigger': 'retreivingTimeout', 'source': 'Retreiving', 'dest': 'CheckObject'},
    {'trigger': 'objectDetected', 'source': 'CheckObject', 'dest': 'AnalyzeObject'},
    {'trigger': 'emptyDetected', 'source': 'CheckObject', 'dest': 'Retreiving'},

    # Transitions for parallel states and splits from State5
    {'trigger': 'isRedBall', 'source': 'AnalyzeObject', 'dest': 'SelectRedBall'},
    {'trigger': 'isGreenBall', 'source': 'AnalyzeObject', 'dest': 'SelectGreenBall'},
    {'trigger': 'isCube', 'source': 'AnalyzeObject', 'dest': 'SelectCube'},

    {'trigger': 'trainTimeout', 'source': 'SelectRedBall', 'dest': 'Dispense'},
    {'trigger': 'trainTimeout', 'source': 'SelectGreenBall', 'dest': 'Dispense'},
    {'trigger': 'trainTimeout', 'source': 'SelectCube', 'dest': 'Dispense'},

    {'trigger': 'dispenseTimeout', 'source': 'Dispense', 'dest': 'Close'},
]

# Initialize the state machine
model = Model()
machine = Machine(model=model, states=states, transitions=transitions, initial='Init')


def main():
    global model
    keyboard.init()

    last_time = time.time()

    last_state = None   # For debug
    try:
        while True:
            if (last_state != model.state):
                print('Entered state ', model.state)

            switch (model.state):
                case 'Ini'
            
            if (key == 'f'):
                model.start()
            
            if not param.keep_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.stop()

if __name__ == "__main__":
    main()

