#% Materia: Procesamiento Digital de Imágenes
#% Proyecto: Trabajo Práctico N° 2 - PROBLEMA 2
#% Alumna: Suligoy, Julia

#% -- Librerias
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.util import invert #Libreria extra


#% -- Funciones
# Defininimos fuinción para mostrar imágenes
def imshow(img, title=None, color_img=False, blocking=False):
    plt.figure()
    if color_img:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.show(block=blocking)

#Defino funcion de Imadjust()
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


#% -- Cargo Imagen 
f = cv2.imread('src/monedas.jpeg')            # Leemos imagen
f = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
# imshow(f, 'Imagen original',color_img=True)

#% -- A
#RGB a escala de grises
f_gray = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)   
# imshow(f_gray, 'En niveles de grises')

#ajuste
f_just = imadjust(f_gray,gamma=1.5)   
# imshow(f_just, 'Colores ajustados')

#filtro pasabajos
f_blur = cv2.GaussianBlur(f_just,(11,11),2.5)
# imshow(f_blur, 'Filtro')

#segmentacion
f_can = cv2.Canny(f_blur, threshold1=0.0001*255, threshold2=0.19*255)
# imshow(f_can,'Canny')

#Morfología - Dilatación
B = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(21,21))
f_dilat = cv2.dilate(f_can,B,iterations = 1)
# imshow(f_dilat,'Dilatación')

#Closing
f_dc = cv2.morphologyEx(f_dilat, cv2.MORPH_CLOSE, B)
# imshow(f_dc,'Dilatación + closing')

#Rellenado
def fillhole(input_image):
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

f_rell =fillhole(f_dc)
# imshow(f_rell,'Relleno huecos')

#Erosión
Be = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(40,40))
f_ero = cv2.erode(f_rell,Be,iterations = 1)
# imshow(f_ero,'Erosion')

#Detección de objetos
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(f_ero, 8)
labels_color = cv2.applyColorMap(np.uint8(255/num_labels*labels), cv2.COLORMAP_MAGMA)
# imshow(labels_color, color_img=True, title=f'Elementos detectados: {num_labels}')

# Contornos
contours, hierarchy = cv2.findContours(f_ero, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) 
mm = cv2.merge((f_ero,f_ero,f_ero))
cv2.drawContours(mm, contours, contourIdx=-1, color=(0, 0, 255), thickness=1) 
imshow(mm, color_img=True, title='Elementos detectados + Contornos')

#Clasificación
# rho = perim**2 / area
# Cuadrado = (4.L)**2 / L**2 = 16.L**2 / L**2 = 16
# Circulo  = (pi.2.R)**2 / (pi.R**2) = 4.pi**2.R**2 / pi.R**2 = 4.pi = 12.56
X = [[]]*num_labels
for ii in range(1,num_labels):
    # -- Obtengo el objeto y lo acondiciono ---------------------------------------
    obj = labels==ii
    obj8 = np.uint8((labels==ii)*255)
    contours, hierarchy = cv2.findContours(obj8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    # -- Calculo características --------------------------------------------------
    area = np.sum(obj8>0)
    perimetro = cv2.arcLength(contours[0],True) 
    rho = (perimetro**2)/area
    # --- Guardo para analizar -------------------------------------------------------------------------------
    X[ii] = {'rho':rho, 'centroid':centroids[ii], 'perimetro': perimetro}

aux = ((labels>0)*255).astype(np.uint8)
img = cv2.merge((aux, aux, aux))
for ii in range(1,num_labels):
    cv2.putText(img, f'{X[ii]["rho"]:5.2f}', (X[ii]['centroid'][0].astype(int), X[ii]['centroid'][1].astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (255,0,0), 0)
imshow(img, title='rho')

Lc = np.zeros(labels.shape, dtype="uint8")  # Imagen donde estarán las etiquetas de los diferentes objetos
etiquetas = np.zeros(num_labels)            # Etiquetas de cada objeto conectado
cant_monedas = {'diez':0,'cincuenta':0,'uno':0}
for ii in range(1,num_labels):
    if X[ii]['rho'] < 16:           # --> Son circulos 
        if X[ii]['perimetro'] < 905:
            Lc[labels==ii] = 1      # $0.10
            etiquetas[ii] = 1
            cant_monedas['diez'] += 1
        elif X[ii]['perimetro'] < 1113:
            Lc[labels==ii] = 2      # $1
            etiquetas[ii] = 2
            cant_monedas['uno'] += 1
        else:
            Lc[labels==ii] = 3      # $0.50
            etiquetas[ii] = 3  
            cant_monedas['cincuenta'] += 1
    else:                           # --> Son cuadrados
        Lc[labels==ii] = 4      
        etiquetas[ii] = 4

# Muestro 
imshow(Lc, title='Clasificación - escala de grises')
Lc_gray = ((Lc/Lc.max())*255).astype('uint8')
imshow(Lc_gray, title='Clasificación - escala de grises')
Lc_color = cv2.applyColorMap(Lc_gray, cv2.COLORMAP_TURBO)
imshow(Lc_color, title='Clasificación - Colores')


#% -- B
print('Conteo de monedas: ', cant_monedas)


#% -- C
#Obtención de la máscara de los dadospara procesar unicamente los dados 
mask = Lc==4
imshow(mask)
dados = f_just*mask
imshow(dados)

# Binarizo
_, binary_img = cv2.threshold(dados, 140, 1, cv2.THRESH_BINARY)  #umbralizar
imshow(binary_img, 'Imagen binaria')

#Closing
bin = invert(binary_img)
d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(5,5))
f_dc = cv2.morphologyEx(bin, cv2.MORPH_CLOSE, d)
imshow(f_dc)
fin = invert(f_dc)
f_ = cv2.morphologyEx(fin, cv2.MORPH_CLOSE, d)
imshow(f_)

#Cuenta el valor del dado a partir de los contornos hijos
contours, hierarchy = cv2.findContours(f_, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(f_, 8)
valor=[]
for pp in range(len(contours)):
    cont=0
    if hierarchy[0][pp][3]==-1:
        # cv2.drawContours(f_, contours, contourIdx=pp, color=(0, 255, 0), thickness=2)
        for ii in range(len(contours)):
            if hierarchy[0][ii][3]==pp:
                cont+=1
                # cv2.drawContours(f_, contours, contourIdx=pp, color=(0, 0, 255), thickness=2)
        valor.append(cont) 
        # cv2.putText(f_, f'{cont}', (centroids[0].astype(int), centroids[1].astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (255,0,0), 0)   
imshow(f_)
print('Número que presenta cada dado:', valor)
