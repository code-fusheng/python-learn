import cv2
import time
import schedule


def startRecord():
    # import time
    # 获取相机
    cap = cv2.VideoCapture(0)
    # 获取视频长宽fps，编码方式
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # 编码方式
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    # 写入视频
    # time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # loca=time.strftime('%Y-%m-%d %H:%M:%S')
    # print(loca)
    # time = 'r\'D:\{}.mp4\''.format(time)
    # print(time)
    out = cv2.VideoWriter(r'D:\t.mp4', fourcc, 24, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret:
            print("打开摄像头失败")
        # frame = cv2.flip(frame, 1)
        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        out.write(frame)
        if key == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


schedule.every(1).minutes.do(startRecord)
while True:
    schedule.run_pending()

