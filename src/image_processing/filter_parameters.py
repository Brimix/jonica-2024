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

saturation_ths              = 85
value_ths                   = 63
sat_val_resolution          = 2

def tweak_by_key(key):
    global blur_intensity, blur_intensity_resolution
    global canny_ths_L, canny_ths_L_resolution
    global canny_ths_H, canny_ths_H_resolution
    global expansion_size, expansion_size_resolution, expansion_size_max
    global erosion_size, erosion_size_resolution, erosion_size_max
    global saturation_ths, value_ths, sat_val_resolution

    if key == 'w':
        blur_intensity += blur_intensity_resolution
    if key == 's' and blur_intensity > blur_intensity_resolution:
        blur_intensity -= blur_intensity_resolution

    if key == 'e' and canny_ths_L + canny_ths_L_resolution < 255:
        canny_ths_L += canny_ths_L_resolution
    if key == 'd' and canny_ths_L > canny_ths_L_resolution:
        canny_ths_L -= canny_ths_L_resolution

    if key == 'r' and canny_ths_H + canny_ths_H_resolution < 255:
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

def show():
    print('---FILTER---')
    print('[h-y] Saturation threshold:    ', saturation_ths)
    print('[j-u] Value threshold:         ', value_ths)
    print('[s-w] Blur intensity:          ', blur_intensity)
    print('[d-e] Canny threshold - Low:   ', canny_ths_L)
    print('[f-r] Canny threshold - High:  ', canny_ths_H)
    print('[g-t] Expansion size:          ', expansion_size)
    print('[k-i] Erosion size:            ', erosion_size)
    print('___FILTER___')
