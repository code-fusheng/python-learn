import cv2 as cv

if __name__ == '__main__':

    # cap = cv.VideoCapture(0)
    capRead = cv.VideoCapture(0)

    width = int(capRead.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(capRead.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = round(capRead.get(cv.CAP_PROP_FPS))
    frameCount = int(capRead.get(cv.CAP_PROP_FRAME_COUNT))
    print(height, width, fps, frameCount)

    # 创建视频写入对象
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    videoWrite = "source/video/video_save_1.avi"
    capWrite = cv.VideoWriter(videoWrite, fourcc, fps, (width, height))

    frameNum = 0
    sn = 0  # 抓拍序号
    timef = 30

    while capRead.isOpened():
        ret, frame = capRead.read()
        if not ret:
            print("无法读取摄像头 frameNum {}".format(frameNum))
            break
        frameNum += 1
        cv.imshow("Camera", frame)
        # if (frameNum % timef == 0):
        capWrite.write(frame)
        key = cv.waitKey(1)
        if key == ord('c'):
            filePath = "source/images/photo_{:d}.png".format(sn)
            cv.imwrite(filePath, frame)
            sn += 1
            print(filePath)
        if key == ord('q'):
            break
    capRead.release()
    capWrite.release()
    cv.destroyAllWindows()

