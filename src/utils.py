import cv2
import torch
import numpy as np


def get_device(device: str):
    if device is None:
        return torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    return torch.device(device)


def get_mask_rcnn(weights, box_conf_th: float, nms_th: float, device):
    model = torch.load(weights, map_location=device)
    model.roi_heads.score_thresh = box_conf_th
    model.roi_heads.nms_thresh = nms_th
    model.eval()
    return model

def get_yolov5(weights, box_conf_th: float, nms_th: float, amp: bool, device):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, device=device)  # local model
    model.conf = box_conf_th  # NMS confidence threshold
    model.iou = nms_th        # NMS IoU threshold
    model.amp = amp           # Automatic Mixed Precision (AMP) inference
    model.eval()
    return model


def get_contour(mask):
    contours, _ = cv2.findContours((mask * 255).astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours[0]


def visualize_semantic_segmentation(img_from_camera, pred):
    mixed = np.where(pred > 240, cv2.addWeighted(img_from_camera, 0.4, pred, 0.6, 1.0), img_from_camera)
    return mixed


def plot_coals_contours_on_img(img, coals: list):
    img_with_contours = np.copy(img)
    for coal2plot in coals:
        coal2plot.plot_on(img_with_contours)
    return img_with_contours
