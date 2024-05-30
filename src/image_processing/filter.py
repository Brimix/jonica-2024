import cv2
import numpy as np
import image_processing.filter_parameters as param

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

def bw_adjust(x, vin=[None,None], vout=[0,255], gamma=1.5):
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

def hsv_adjust(img, sat_thresh=30, val_thresh=30):
    """
    Adjust an HSV image to set pixels to black where saturation or value is below a threshold.

    :param image: Input image in HSV format (H, S, V channels).
    :param sat_thresh: Saturation threshold below which pixels are set to black.
    :param val_thresh: Value threshold below which pixels are set to black.
    :return: Adjusted image.
    """

    # Check if the image is in the correct format
    if img.dtype != np.uint8:
        raise ValueError("Image should be in uint8 format")

    # Split into individual channels
    H, S, V = cv2.split(img)

    # Create a mask where saturation and value are below the respective thresholds
    mask = (S < param.saturation_ths) | (V < param.value_ths)

    # Apply the mask to a copy of the HSV image
    img_copy = img.copy()
    img_copy[mask] = 0  # Setting all channels to 0 turns the pixel black

    return img_copy

def blur(img):
    return cv2.GaussianBlur(img,(5,5), param.blur_intensity)

def segment(img):
    return cv2.Canny(img, param.canny_ths_L, param.canny_ths_H)

def expand(img):
    struct = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(param.expansion_size, param.expansion_size))
    return cv2.dilate(img, struct, iterations = 1)

def close_shape(img):
    struct = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(param.expansion_size, param.expansion_size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, struct)

def open_shape(img):
    struct = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(param.expansion_size, param.expansion_size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, struct, iterations=2)

def fill_holes(img):
    '''
    input gray binary image  get the filled image by floodfill method
    '''
    im_flood_fill = img.copy()
    h, w = img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    im_flood_fill = im_flood_fill.astype("uint8")
    cv2.floodFill(im_flood_fill, mask, (0, 0), 255)
    im_flood_fill_inv = cv2.bitwise_not(im_flood_fill)
    img_out = img | im_flood_fill_inv
    return img_out

def erode(img):
    struct = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (param.erosion_size, param.erosion_size))
    return cv2.erode(img, struct, iterations = 1)
