import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from .u2net.model import *
from .u2net.utils import *
from .tracer.config import *
from .tracer.tracer import *
import torch.nn as nn

# pip install torch torchvision PIL numpy


device_info = "cpu"
if torch.cuda.is_available():
    device_info = "cuda:0"


def load_model(model_name="U2NET", model_path=None):
    if model_path is None:
    	print("Empty path")
    	exit()

    if model_name == "U2NET":
        # Input Image Size
        size = 320

        # model_path = './ckpt/u2net.pth'
        model_pred = U2NET(3, 1)
        model_pred.load_state_dict(torch.load(model_path, map_location=device_info))
        model_pred.eval()
    elif model_name == "TRACER":
        # Input Image Size
        size = 640

        if torch.cuda.is_available() == False:
        	print("Error! Only cuda")
        	exit()

        cfg = getConfig()
        # model_path = './ckpt/TRACER-Efficient-8.pth'
        model_pred = TRACER(cfg).to(device_info)
        model_pred = nn.DataParallel(model_pred).to(device_info)
        model_pred.load_state_dict(torch.load(model_path, map_location=device_info), strict=False)
        model_pred.eval()
    else:
        print("Unknown Model")
        exit()
    return model_pred


def norm_pred(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)
    return dn


def preprocess(image, size):
    label_3 = np.zeros(image.shape)
    label = np.zeros(label_3.shape[0:2])

    if 3 == len(label_3.shape):
        label = label_3[:, :, 0]
    elif 2 == len(label_3.shape):
        label = label_3

    if 3 == len(image.shape) and 2 == len(label.shape):
        label = label[:, :, np.newaxis]
    elif 2 == len(image.shape) and 2 == len(label.shape):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]


    transform = transforms.Compose([RescaleT(size), ToTensorLab(flag=0)])
    sample = transform({"imidx": np.array([0]), "image": image, "label": label})

    return sample


def remove_bg(image, model="U2NET", model_pred=None):

    # Upload weights

    # image = PIL Image

    if model_pred == None:
        print("Error. Please load model!")
        exit()

    size = 320
    if model == "TRACER":
        size = 640

    sample = preprocess(np.array(image), size)

    with torch.no_grad():
        inputs_test = torch.FloatTensor(sample["image"].unsqueeze(0).float())

        if model == "U2NET":
            d1, _, _, _, _, _, _ = model_pred(inputs_test)
        else:
            d1, _, _ = model_pred(inputs_test)
        torch.cuda.empty_cache()
        pred = d1[:, 0, :, :]
        predict = norm_pred(pred).squeeze().cpu().detach().numpy()
        img_out = Image.fromarray(predict * 255).convert("RGB")
        img_out = img_out.resize((image.size), resample=Image.BILINEAR)
        empty_img = Image.new("RGBA", (image.size), 0)
        img_out = Image.composite(image, empty_img, img_out.convert("L"))
        del d1, pred, predict, inputs_test, sample

        return img_out