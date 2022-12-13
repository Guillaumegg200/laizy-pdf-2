import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

import os
import numpy as np
import torch
import torch.utils.data
from PIL import Image
import json

# from detector.engine import train_one_epoch, evaluate
# import detector.utils
# import detector.transforms as T
from engine import train_one_epoch, evaluate
import utils
import transforms as T

def remove_empty_annotation(json):
    """
    Given a json file to train, this function will remove image without annotations to avoid any bug duriong the training

    Input :
    json file

    Output :
    json file
    """
    file_to_remove = []
    for filename in json.keys():
        if json[filename]["regions"] == []:
            file_to_remove.append(filename)
    for filename in file_to_remove:
        del json[filename]
    return json

class SectionDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, transforms=None):
        self.data_dir = data_dir
        self.transforms = transforms
        # load the annotations file, it also contain information of image names
        # load annotations
        annotations1 = json.load(open(os.path.join(data_dir, "via_section_data.json")))
        annotations1 = remove_empty_annotation(annotations1)
        self.annotations = list(annotations1.values())  # don't need the dict keys
        

    def __getitem__(self, idx):

        # get the image path from the annoations data
        img_name = self.annotations[idx]["filename"]
        print(img_name)
        img_path = os.path.join(self.data_dir, img_name)
        img = Image.open(img_path).convert("RGB")
        
        # first id is the background, objects count from 1
        obj_ids = np.array(range(len(self.annotations[idx]["regions"]))) +1
        # get bounding box coordinates for each object
        num_objs = len(obj_ids)
        boxes = []

        for i in range(num_objs):
            x = self.annotations[idx]["regions"][i]["shape_attributes"]["x"]
            width = self.annotations[idx]["regions"][i]["shape_attributes"]["width"]
            y = self.annotations[idx]["regions"][i]["shape_attributes"]["y"]
            height = self.annotations[idx]["regions"][i]["shape_attributes"]["height"]
            boxes.append([x, y, x + width , y + height])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.annotations)

class ItemDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, transforms=None):
        self.data_dir = data_dir
        self.transforms = transforms
        # load the annotations file, it also contain information of image names
        # load annotations
        annotations1 = json.load(open(os.path.join(data_dir, "via_item_data.json")))
        annotations1 = remove_empty_annotation(annotations1)

        self.annotations = list(annotations1.values())  # don't need the dict keys
        

    def __getitem__(self, idx):

        # get the image path from the annoations data
        img_name = self.annotations[idx]["filename"]
        print(img_name)
        img_path = os.path.join(self.data_dir, img_name)
        img = Image.open(img_path).convert("RGB")
        
        # first id is the background, objects count from 1
        obj_ids = np.array(range(len(self.annotations[idx]["regions"]))) +1
        # get bounding box coordinates for each object
        num_objs = len(obj_ids)
        boxes = []

        for i in range(num_objs):
            x = self.annotations[idx]["regions"][i]["shape_attributes"]["x"]
            width = self.annotations[idx]["regions"][i]["shape_attributes"]["width"]
            y = self.annotations[idx]["regions"][i]["shape_attributes"]["y"]
            height = self.annotations[idx]["regions"][i]["shape_attributes"]["height"]
            boxes.append([x, y, x + width , y + height])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.annotations)

def build_model(num_classes):
    # load an instance segmentation model pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

    # get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

def get_transform(train):
    transforms = []
    # converts the image, a PIL image, into a PyTorch Tensor
    transforms.append(T.ToTensor())
    if train:
        # during training, randomly flip the training images
        # and ground-truth for data augmentation
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)

def train_item_model(output_path):

    # use our dataset and defined transformations
    dataset = ItemDataset('./Dataset copy/train', get_transform(train=True))
    dataset_test = ItemDataset('./Dataset copy/val', get_transform(train=False))

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # our dataset has two classes only - background and beagle
    num_classes = 2

    # get the model using our helper function
    model = build_model(num_classes)
    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)

    # and a learning rate scheduler which decreases the learning rate by
    # 10x every 3 epochs
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)
    
    # number of epochs
    num_epochs = 10
    #start training
    for epoch in range(num_epochs):
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
        # update the learning rate
        lr_scheduler.step()
        # evaluate on the test dataset
        evaluate(model, data_loader_test, device=device)
    
    # save trained model for inference    
    torch.save(model,output_path )

def train_section_model(output_path):

    # use our dataset and defined transformations
    dataset = SectionDataset('./Dataset copy/train', get_transform(train=True))
    dataset_test = SectionDataset('./Dataset copy/train', get_transform(train=False))

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # our dataset has two classes only - background and beagle
    num_classes = 2

    # get the model using our helper function
    model = build_model(num_classes)
    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)

    # and a learning rate scheduler which decreases the learning rate by
    # 10x every 3 epochs
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)
    
    # number of epochs
    num_epochs = 10
    #start training
    for epoch in range(num_epochs):
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
        # update the learning rate
        lr_scheduler.step()
        # evaluate on the test dataset
        evaluate(model, data_loader_test, device=device)
    
    # save trained model for inference    
    torch.save(model,output_path )
if __name__ == "__main__":

    ## ITEM
    #train_item_model('./output/faster-rcnn-item-2.pt')
    #train_section_model('./output/faster-rcnn-section-2.pt')
    pass