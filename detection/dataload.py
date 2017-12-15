from __future__ import print_function
import numpy as np

import os
from os.path import join

from torch.utils import data

from torchvision import transforms, datasets

from PIL import Image


class Markers(data.Dataset):
    """
    Do not use a torch resizing transform with this dataset as that is slow.
    Instead, run resize_ISIC.py from scripts_retrieval to resize
    images prior to training.
    """
    def __init__(self, train=True, transform=None):
        self.root = join(os.getcwd(), 'resources')
        self.filename='images'
        self.transform=transform
        self.train = train
        self.traindata = []
        self.trainlabels = []
        self.testdata = []
        self.testlabels = []
        if self.train:
            f = open(join(self.root, 'trainlabels.txt'), 'r')
            file = f.readlines()
            for line in file:
                filename = line.split(',')[0]
                label = line.split(',')[1]
                self.traindata.append(join(self.root, self.filename, 'train', filename))
                self.trainlabels.append(np.float32(label))

        else:
            f = open(join(self.root, 'testlabels.txt'), 'r')
            file = f.readlines()
            for line in file:
                filename = line.split(',')[0]
                label = line.split(',')[1]
                self.testdata.append(join(self.root, self.filename, 'test', filename))
                self.testlabels.append(np.float32(label))



    def __getitem__(self, index):
        if self.train:
            img = Image.open(self.traindata[index])
            label = self.trainlabels[index]
        else:
            img = Image.open(self.testdata[index])
            label = self.testlabels[index]
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        if self.train:
            return len(self.traindata)
        else:
            return len(self.testdata)
