Este es un "plug and play" de la RNN, solo se encuentra la red ya entrenada (40epochs 0.001 learning rate) y el respectivo main para analizar las imagenes.

Instrucciones de uso:
-Colocar una imagen en test_image con el nombre output_camara.png de 28x28 pixeles.
-ajustar en el script la ubicación de la Network en tu computadora y del path del test_image
-Correr el script en main.py



CONSIDERACIONES!!!:
-todo esto fue entrenado por separado, te adjunté en otro folder todo lo utilizado
-Realizé deformaciones a las imagenes iniciales para entrenarla y mejoraron los resultados, las podria deformar aun mas(achicar y agrandar mas) y solventar las siguientes dificultades:
	-Los circulos deben ser suficientemente grandes, si son muy chicos tiene problemas ( mi suposicion es que ve lineas de pixeles rectos debido a su resolucion)
	-Vi que tenia problemas con cuadrados que ocupan todo el espacio de trabajo.

