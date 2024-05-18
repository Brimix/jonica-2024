# Execution parameters
keep_running                = True
cam_debug                   = False  # If true, displays camera preview
frame_timespan              = 5     # Seconds between shots

# Servo parameters
angle_min                   = 0
angle_max                   = 180
angle                       = 45
angle_resolution            = 45

# Filters' parameters (can be tweaked)
blur_intensity              = 6.1
blur_intensity_resolution   = 0.2

canny_ths_L                 = 0.08*255
canny_ths_L_resolution      = 0.01*255

canny_ths_H                 = 0.45*255
canny_ths_H_resolution      = 0.01*255

expansion_size              = 5
expansion_size_resolution   = 1
expansion_size_max          = 100

erosion_size                = 19
erosion_size_resolution     = 2
erosion_size_max            = 100

saturation_ths              = 55
value_ths                   = 81
sat_val_resolution          = 2



def tweak_by_key(key):
    global keep_running
    global blur_intensity, blur_intensity_resolution
    global canny_ths_L, canny_ths_L_resolution
    global canny_ths_H, canny_ths_H_resolution
    global angle, angle_min, angle_max, angle_resolution
    global expansion_size, expansion_size_resolution, expansion_size_max
    global erosion_size, erosion_size_resolution, erosion_size_max
    global saturation_ths, value_ths, sat_val_resolution

    if key == 'q':
        keep_running = False

    if key == 'w':
        blur_intensity += blur_intensity_resolution
    if key == 's' and blur_intensity > blur_intensity_resolution:
        blur_intensity -= blur_intensity_resolution

    if key == 'e' and canny_ths_L + canny_ths_L_resolution < 255:
        canny_ths_L += canny_ths_L_resolution
    if key == 'd' and canny_ths_L > canny_ths_L_resolution:
        canny_ths_L -= canny_ths_L_resolution

    if key == 'r' and canny_ths_L + canny_ths_H_resolution < 255:
        canny_ths_H += canny_ths_H_resolution
    if key == 'f' and canny_ths_H > canny_ths_H_resolution:
        canny_ths_H -= canny_ths_H_resolution

    if key == 't' and expansion_size + expansion_size_resolution < expansion_size_max:
        expansion_size += expansion_size_resolution
    if key == 'g' and expansion_size - expansion_size_resolution > 0:
        expansion_size -= expansion_size_resolution

    if key == 'y' and saturation_ths + sat_val_resolution < 255:
        saturation_ths += sat_val_resolution
    if key == 'h' and saturation_ths > sat_val_resolution:
        saturation_ths -= sat_val_resolution

    if key == 'u' and value_ths + sat_val_resolution < 255:
        value_ths += sat_val_resolution
    if key == 'j' and value_ths > sat_val_resolution:
        value_ths -= sat_val_resolution

    if key == 'i' and erosion_size + erosion_size_resolution < erosion_size_max:
        erosion_size += erosion_size_resolution
    if key == 'k' and erosion_size - erosion_size_resolution > 0:
        erosion_size -= erosion_size_resolution

    if key == 'p' and angle + angle_resolution <= angle_max:
        angle += angle_resolution
    if key == 'o' and angle - angle_resolution >= angle_min:
        angle -= angle_resolution

def show():
    print('---')
    print('Saturation threshold:    ', saturation_ths)
    print('Value threshold:         ', value_ths)
    print('Blur intensity:          ', blur_intensity)
    print('Canny threshold - Low:   ', canny_ths_L)
    print('Canny threshold - High:  ', canny_ths_H)
    print('Expansion size:          ', expansion_size)
    print('Erosion size:            ', erosion_size)
    print('---')
    print('Servo angle:             ', angle)
