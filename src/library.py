import cv2
import numpy as np

def library_toGray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def imadjust(x, vin=[None,None], vout=[0,255], gamma=1):
    # x      : Imagen de entrada en escalas de grises (2D), formato uint8.
    # vin    : Límites de los valores de intensidad de la imagen de entrada
    # vout   : Límites de los valores de intensidad de la imagen de salida
    # y      : Imagen de salida
    if vin[0]==None:
        vin[0] = x.min()
    if vin[1]==None:
        vin[1] = x.max()
    y = (((x - vin[0]) / (vin[1] - vin[0])) ** gamma) * (vout[1] - vout[0]) + vout[0]
    y[x<vin[0]] = vout[0]   # Valores menores que low_in se mapean a low_out
    y[x>vin[1]] = vout[1]   # Valores mayores que high_in se mapean a high_out
    if x.dtype==np.uint8:
        y = np.uint8(np.clip(y+0.5,0,255))   # Numpy underflows/overflows para valores fuera de rango, se debe utilizar clip.
    return y

def library_adjust(img):
    return imadjust(img,gamma=1.5)

def library_filter(img, intensity):
    return cv2.GaussianBlur(img,(11,11), intensity)

def library_segment(img):
    return cv2.Canny(img, threshold1 = 0.0001*255, threshold2 = 0.19*255)
