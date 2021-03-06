import os
import random
import torch
from torch.utils.data import Dataset
from torchvision import transforms, utils
from PIL import Image
from skimage import io, transform
import numpy
import torchvision



class PatchDataset(Dataset):
    def __init__(self, x_set, y_set, model_config=None):

        """
        Args:
            x_set (string): List of paths to images
            y_set (int): Labels of each image in x_set
            model_config (dict): Dict of model config.
        """
        self.x_set = x_set
        self.y_set = y_set
        if model_config :
            self.normalize = model_config['normalize']
            if (self.normalize):
                self.transform = transforms.Compose([transforms.ToTensor(),
                                                     transforms.Normalize(mean=model_config['mean'],
                                                                          std=model_config['std'])])
        else:
            self.normalize= False

        self.length = len(x_set)
        if len(x_set) != len(y_set):
            raise ValueError('x set length does not match y set length')

    def __len__(self):
        return self.length        

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        x = Image.open(self.x_set[idx]).convert('RGB')
        #x = x.transpose(2, 0, 1) #if x is np array and it has format Width * Height * Channel
        y = self.y_set[idx]

        if self.normalize:
            x = self.transform(x)
        else :
            x = numpy.asarray(x).copy().transpose(2, 0, 1)
            x = (x - 128.) / 128. # must be in [-1, 1] range
            x = torch.from_numpy(x).type(torch.float)
        return x, torch.tensor(y), self.x_set[idx]
