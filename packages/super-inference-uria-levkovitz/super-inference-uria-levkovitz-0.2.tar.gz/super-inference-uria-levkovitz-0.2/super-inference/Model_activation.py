import os
from torchvision import datasets, transforms,models
from collections import defaultdict
from torch.optim import lr_scheduler

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class Model_activation():

    
    def __init__(self, model_dir = r'C:\Users\urial\BG\AlphaBravo\notebooks\models',model_file_name = 'AllLegs_combined2.pt'):#model_path):# =


        self.model_path = os.path.join(model_dir, model_file_name) #model_path#
    
        model = self.pretrained_resnet18(transfer_learning=True,num_class=9)
        self.model = self.load_model(model)
        
    def pretrained_resnet18(self,transfer_learning=True, num_class=8):
        resnet = models.resnet18(pretrained=True)

        if transfer_learning:
            for param in resnet.parameters():
                param.requires_grad = False

        last_layer_in = resnet.fc.in_features
        resnet.fc = nn.Linear(last_layer_in, num_class)
        return resnet

    def load_model(self,model):#, model_dir='models', model_file_name='AllLegs.pt'
#         model_path = os.path.join(self.model_dir, self.model_file_name)

        # loading the model and getting model parameters by using load_state_dict
        model.load_state_dict(torch.load(self.model_path))

        return model
   
    def image_preprocess_transforms(self):

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor()])

        return preprocess

    def image_common_transforms(self):
            preprocess = self.image_preprocess_transforms()

            common_transforms = transforms.Compose([
                preprocess,
                transforms.Normalize(self.mean, self.std)])
            return common_transforms