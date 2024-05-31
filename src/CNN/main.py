# main.py
import torch
from network import ConvolutionalNeuronalNetwork, load_datasets, train, evaluate, save_model, load_model, preprocess_image

def loadandevaluate(device,val_loader,img_height,img_width,image_path=None): 
    # Cargar el modelo guardado y evaluar nuevamente
    model = ConvolutionalNeuronalNetwork(img_height, img_width)
    load_model(model, r'C:\Users\tomas\OneDrive\Escritorio\Dataset\ConvolutionalNeuronalNetwork.pth', device)
    
    if image_path:
        model.eval()
        image = preprocess_image(image_path, img_height, img_width).to(device)
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output.data, 1)
            if predicted.item() == 1:
                print(f'Predicted class for the image {image_path}: Square')
            elif predicted.item() == 0:
                print(f'Predicted class for the image {image_path}: Circle')
    else:
        val_accuracy = evaluate(model, val_loader, device)
        print(f'Loaded Model Validation Accuracy: {val_accuracy:.2f}%')


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    img_height, img_width = 28, 28
    batch_size = 32                     # tamaño del batch con el cual se entrenan las imagenes, es un parametro a variar dado que modifica el aprendizaje de la red neuronal
    validation_split = 0.2              #20% para validación
    test_split = 0.1                    #10% para test final

    # Cargar conjuntos de datos
    train_loader, val_loader, test_loader = load_datasets(
        root_dir=r'C:\Users\tomas\OneDrive\Escritorio\Dataset\images',
        img_height=img_height,
        img_width=img_width,
        batch_size=batch_size,
        validation_split=validation_split,
        test_split=test_split
    )

    # Crear modelo
    model = ConvolutionalNeuronalNetwork(img_height, img_width).to(device)

    # Definir función de pérdida y optimizador
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    num_epochs = 40
    # Entrenar modelo
    train(model, train_loader, criterion, optimizer, device, num_epochs)

    # Guardar el modelo entrenado
    save_model(model, r'C:\Users\tomas\OneDrive\Escritorio\Dataset\ConvolutionalNeuronalNetwork.pth')

    # Evaluar modelo en conjunto de validación (ajustar métricas lr, epochs, optimizer, criterio)
    val_accuracy = evaluate(model, val_loader, device)
    print(f'Validation Accuracy: {val_accuracy:.2f}%')

    # Evaluar modelo en conjunto de prueba (estos datos son los que nunca vió el modelo)
    test_accuracy = evaluate(model, test_loader, device)
    print(f'Test Accuracy: {test_accuracy:.2f}%')

    # Cargar el modelo guardado y evaluar nuevamente (opcional): esta hecho para utilizar en la Raspi y no tener que andar entrenando nuevamente todo.
    loadandevaluate(device,val_loader,img_height,img_width,r'C:\Users\tomas\OneDrive\Escritorio\Dataset\camara\test.png')
    
 #  NOTAS:
 # La CNN es básica pero puede cumplir, noté que cuando le presentaba circulos de tamaños mas pqueños los identificaba como cuadrados lo cual es un problema (y la posible causa 
 # en los datos de entrenamiento los tamaños de los simbolos son relativemente constantes)

 # El modelo subido a github fue entrenado con lr 0.001 y 40 epochs (por lo general se recomendaba entrenar un numero alto de epocas)

 # la funcion loadandevaluate carga imagenes de otro folder distinto y las evalua

 # Al codigo le falta modularizarlo 20 mil veces, pero son las 3 am y no tengo tiempo. A load and evaluate estaria bueno pasarle como parametros el img_file_path y el model_path


if __name__ == '__main__':
    main()