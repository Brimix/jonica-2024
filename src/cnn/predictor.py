import cv2
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

def load_and_evaluate(device,img_height,img_width,cv_image=None,network_path=None): 
    model = ConvolutionalNeuronalNetwork(img_height, img_width).to(device)
    load_model(model,network_path, device)

    # if cv_image[0]:
    model.eval()
    image = preprocess_image(cv_image, img_height, img_width).to(device)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output.data, 1)
        if predicted.item() == 1:
            return 'square'
        elif predicted.item() == 0:
            return 'circle'

def preprocess_image(cv_image, img_height, img_width):
    image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    # Convert the NumPy image array to a PIL Image
    pil_image = Image.fromarray(image_rgb)

    transform = transforms.Compose([
        transforms.Resize((img_height, img_width)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    image = transform(pil_image).unsqueeze(0)
    return image


def load_model(model, path, device):
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    return model

def predict_from_image(cv_image):
    # Ajustar el img height y el width en funcion de la red neuronal utilizada (200x200 o 28x28)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    img_height, img_width = 28, 28

    # img_path = r'/home/cafe/jonica-2024/src/cnn/test_image/output_camara.png'
    nn_path = r'/home/cafe/jonica-2024/src/cnn/networks/cnn-30epochs-28x28-high-reshape.pth'
    
    return load_and_evaluate(device,img_height,img_width, cv_image, nn_path)
