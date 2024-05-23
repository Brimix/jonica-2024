# Execution parameters
keep_running                = True
frame_timespan              = 6     # Seconds between shots

# Servo parameters
angle_min                   = 0
angle_max                   = 180
angle                       = 0
angle_resolution            = 10

def tweak_by_key(key):
    global keep_running
    global angle, angle_min, angle_max, angle_resolution

    if key == 'q':
        keep_running = False
    if key == 'p' and angle + angle_resolution <= angle_max:
        angle += angle_resolution
    if key == 'o' and angle - angle_resolution >= angle_min:
        angle -= angle_resolution

def show():
    print('---SERVO---')
    print('Servo angle:             ', angle)
    print('___SERVO___')
