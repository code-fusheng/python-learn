from ultralytics import YOLO

import cv2
import matplotlib.pyplot as plt

import torch
# 有 GPU 就用 GPU，没有就用 CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('device:', device)

# 载入预训练模型
# model = YOLO('yolov8n.pt')
# model = YOLO('yolov8s.pt')
# model = YOLO('yolov8m.pt')
# model = YOLO('yolov8l.pt')
# model = YOLO('yolov8x.pt')
model = YOLO('yolov8x.pt')

model.to(device)
model.cpu()  # CPU
# model.cuda() # GPU

deviceInfo = model.device
print(deviceInfo)
print(model.names)

# 传入数据
img_path = 'images/full_冀R17BZ1_20230620030654064.jpg'
rtsp_path = 'rtsp://10.168.1.2:8557/h264'

results = model.predict(source=img_path, save=True, show=True)

# results = model.predict(source=rtsp_path, show=True)