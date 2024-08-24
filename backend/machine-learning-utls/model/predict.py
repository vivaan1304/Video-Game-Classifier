from torchvision import models
import torch.utils.data
from torch import nn
from PIL import Image
import torchvision
import torch

game = ['Among Us', 'Apex Legends', 'Fortnite', 'Forza', 'Free Fire', 'Genshin Impact', 'God of War', 'Minecraft', 'Roblox', 'Terraria']
MODEL_DIR = "/home/vivaan/Desktop/projects/Machine+DeepLearning/video-game-classifier/Video-Game-Classifier/backend/machine-learning-utls/model/model.pth"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def predict():
    model_ft = models.regnet_x_800mf()
    num_ftrs = model_ft.fc.in_features

    model_ft.fc = nn.Linear(num_ftrs, len(range(10)))
    model_ft = model_ft.to(device)
    model_ft.load_state_dict(torch.load(MODEL_DIR))
    model_ft.eval()
    with torch.no_grad():
        with Image.open('/home/vivaan/Desktop/projects/Machine+DeepLearning/video-game-classifier/Video-Game-Classifier/backend/flask-app/templates/static/image.jpeg') as img:
            transforms = torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            img = transforms(img)
            img = img.unsqueeze(0)
            img = img.to(device)
            out = model_ft(img)
            _, pred = torch.max(out, 1)
            return game[pred[0]]

