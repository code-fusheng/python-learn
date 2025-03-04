import cv2
import numpy as np

def test_open_rtsp():
    cap = cv2.VideoCapture("rtsp://10.168.1.2:8557/h264", cv2.CAP_MSMF)
    if cap.isOpened():
        print("yes")
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        rval, frame = cap.read()
        while rval:
            cv2.setWindowTitle("test", "1")
        cv2.imshow('windows', frame)
        cv2.waitKey(int(1000 / int(fps)))
        rval, frame = cap.read()
    else:
        print("no")

def test_play_rtsp():
    rtsp_url = 'rtsp://10.168.1.2:8557/h264'
    # url = 0
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    while True:
        # 读取一帧图像
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        ret, frame = cap.read()
        print(ret)
        # 检查是否成功读取到图像（ret为True表示成功）
        if not ret:
            print("Error reading frame.")
            break
        # 显示视频帧
        cv2.imshow('RTSP Video Stream', frame)
        # 按'q'键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 清理资源
    cap.release()
    cv2.destroyAllWindows()

def test_play_rtsp_pro(rtsp_urls):
    frames = []
    video_caps = [cv2.VideoCapture(url) for url in rtsp_urls]

    while True:
        # 读取每一组RTSP流的一帧
        for i, cap in enumerate(video_caps):
            ret, frame = cap.read()
            if not ret:
                print(f"Error reading frame from RTSP stream {i + 1}.")
                break
            height, width, _ = frame.shape
            resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            frames.append(resized_frame)

        # 如果所有流都成功读取了帧，则拼接并显示
        if len(frames) == len(rtsp_urls):
            # 假设三组视频流分辨率相同，进行水平拼接
            combined_frame = np.hstack([frames[0], frames[1], frames[2]])
            cv2.imshow('Windows', combined_frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break

        # 清空frames列表，准备下一轮循环
        frames.clear()

    # 关闭所有的VideoCapture资源
    for cap in video_caps:
        cap.release()

if __name__ == '__main__':

    rtsp_urls = [
        "rtsp://10.168.1.2:8557/h264",
        # "rtsp://10.168.1.3:8557/h264",
        # "rtsp://10.168.1.4:8557/h264"
    ]

    test_open_rtsp()
    # test_play_rtsp()