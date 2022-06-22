import numpy as np
import argparse
import os
import cv2
from arcface_torch.backbones import get_model
import torch

THRESHOLD = 0.6


def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def find_label(emb_dir, img_path, name, weight):
    labels = []
    dists = []
    img = cv2.imread(img_path)
    img = cv2.resize(img, (112, 112))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2, 0, 1))
    img = torch.from_numpy(img).unsqueeze(0).float()
    img.div_(255).sub_(0.5).div_(0.5)
    net = get_model(name, fp16=False)
    net.load_state_dict(torch.load(weight))
    net.eval()
    feat = net(img).detach().numpy().reshape(512)
    for emb in os.listdir(emb_dir):
        embedding = np.load(emb_dir + f'{emb}').reshape(512)
        dist = findCosineDistance(embedding, feat)

        print(dist)
        if dist < 0.15:
            labels.append(int(emb.split('_')[0]))
            dists.append(dist)
    if len(labels) == 0:
        print('No matching face(s) found in database!')
    else:
        # dist_min = np.min(dists)
        label = labels[np.argmin(dists)]
        print(f'{len(labels)} faces found in the database and have label {label}')


def label_realtime(emb_dir, img, name, weight):
    labels = []
    dists = []
    img = cv2.resize(img, (112, 112))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2, 0, 1))
    img = torch.from_numpy(img).unsqueeze(0).float()
    img.div_(255).sub_(0.5).div_(0.5)
    net = get_model(name, fp16=False)
    net.load_state_dict(torch.load(weight))
    net.eval()

    feat = net(img).detach().numpy().reshape(512)
    for emb in os.listdir(emb_dir):
        embedding = np.load(emb_dir + f'{emb}').reshape(512)
        dist = findCosineDistance(embedding, feat)

        print(dist)
        if dist < 0.15:
            labels.append(int(emb.split('_')[0]))
            dists.append(dist)
    if len(labels) == 0:
        print('No matching face(s) found in database!')
    else:
        # dist_min = np.min(dists)
        label = labels[np.argmin(dists)]
        print(f'{len(labels)} faces found in the database and have label {label}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch ArcFace Training')
    parser.add_argument('--embedding_dir', type=str, default='')
    parser.add_argument('--img_path', type=str, default='')
    parser.add_argument('--network', type=str, default='r100', help='backbone network')
    parser.add_argument('--weight', type=str, default='')
    args = parser.parse_args()
    find_label(args.embedding_dir, args.img_path, args.network, args.weight)
