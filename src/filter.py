import cv2
import numpy as np

def filter_toGray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def filter_toSaturated(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

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

def filter_adjust(img):
    return imadjust(img,gamma=1.5)

def filter_blur(img, intensity):
    return cv2.GaussianBlur(img,(11,11), intensity)

def filter_segment(img, t1, t2):
    return cv2.Canny(img, t1, t2)

def filter_expand(img):
    B = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(21, 21))
    return cv2.dilate(img, B, iterations = 1)

def filter_closeShape(img):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, B)

def filter_fillHoles(img):
    '''
    input gray binary image  get the filled image by floodfill method
    '''
    im_flood_fill = input_image.copy()
    h, w = input_image.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    im_flood_fill = im_flood_fill.astype("uint8")
    cv2.floodFill(im_flood_fill, mask, (0, 0), 255)
    im_flood_fill_inv = cv2.bitwise_not(im_flood_fill)
    img_out = input_image | im_flood_fill_inv
    return img_out 