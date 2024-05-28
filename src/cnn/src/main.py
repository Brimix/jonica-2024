import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

class ConvolutionalNeuronalNetwork(nn.Module):
    def __init__(self, img_height, img_width):
        super(ConvolutionalNeuronalNetwork, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # Assuming images are RGB
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * (img_height // 4) * (img_width // 4), 128),
            nn.ReLU(),
            nn.Linear(128, 2)  # Output for two classes
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

def loadandevaluate(device,img_height,img_width,image_path=None,network_path=None): 
    model = ConvolutionalNeuronalNetwork(img_height, img_width).to(device)
    load_model(model,network_path, device)

    if image_path:
        model.eval()
        image = preprocess_image(image_path, img_height, img_width).to(device)
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output.data, 1)
            if predicted.item() == 1:
                print(f'Predicted class for the image {image_path}: SQUARE')
            elif predicted.item() == 0:
                print(f'Predicted class for the image {image_path}: CIRCLE')

def preprocess_image(image_path, img_height, img_width):
    transform = transforms.Compose([
        transforms.Resize((img_height, img_width)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image


def load_model(model, path, device):
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    return model

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    img_height, img_width = 28, 28
    loadandevaluate(device,img_height,img_width,r'C:\Users\tomas\OneDrive\Escritorio\Test-RNN\code\test_image\output_camara.png', r'C:\Users\tomas\OneDrive\Escritorio\Test-RNN\code\networks\cnn-30epochs-28x28-high-reshape.pth')
    #Ajustar el img height y el width en funcion de la red neuronal utilizada (200x200 o 28x28)
    #Probe con 2 im
if __name__ == '__main__':
    main()
    