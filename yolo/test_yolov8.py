import cv2
from ultralytics import YOLO

# 加载预训练的YOLOv8模型（自动下载或使用本地权重）
model = YOLO("weights/yolov8n.pt")  # 可选模型: yolov8s.pt, yolov8m.pt等
# 打开摄像头（Mac通常为0）
cap = cv2.VideoCapture(0)
while cap.isOpened():
    # 读取摄像头画面
    success, frame = cap.read()
    if not success:
        break
    # 使用YOLOv8进行检测
    results = model.predict(frame)  # 设置置信度阈值
    # 绘制检测结果
    annotated_frame = results[0].plot()
    # 显示实时画面
    cv2.imshow('YOLOv8 Real-Time Detection', annotated_frame)
    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放资源
cap.release()
cv2.destroyAllWindows()