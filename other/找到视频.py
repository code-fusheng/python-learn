import os
import cv2

#传入时间戳
def find(timepoint, name, fourcc, fps, w, h):
    import time
    #拿到年月日进入文件夹中查找
    year = time.localtime(timepoint).tm_year
    month = time.localtime(timepoint).tm_mon
    day = time.localtime(timepoint).tm_mday
    hour = time.localtime(timepoint).tm_hour
    m = time.localtime(timepoint).tm_min
    sec = time.localtime(timepoint).tm_sec
    filepath = "./outputs/{}/{}/{}".format(year, month, day)

    #文件夹存在则继续，否则退出
    if os.path.exists(filepath):
        pass
    else:
        print("文件不存在或已被删除")
        exit(1)
    #遍历该文件夹
    for i, j, k in os.walk(filepath):
        #遍历文件名
        for name in k:
            #去掉后缀
            filename = int(name.split('.')[0])
            #同一小时
            if time.localtime(filename).tm_hour == hour:
                #发生时间分钟比记录时间分钟大
                if m - time.localtime(filename).tm_min > 0:
                    #切片时间点在视频的秒数位置
                    t = (m - time.localtime(filename).tm_min) * 60 + (sec - time.localtime(filename).tm_sec)
                    #准备写入视频
                    video_writer = cv2.VideoWriter("./query/" + name + ".avi", fourcc, fps, (w, h))
                    #读取视频
                    video = filepath + "/" + str(filename) + ".avi"
                    cap = cv2.VideoCapture(video)
                    #计数器
                    count = 0
                    #前置帧：从这开切
                    c1 = fps * (t - 5)
                    #后置帧：到这结束
                    c2 = fps * (t + 5)
                    #开始读取切割
                    #存在问题：按顺序读取，单个视频时间过长会导致切割花费格外时间
                    while cap.isOpened:
                        ret, frame = cap.read()
                        #写入需要帧
                        if (count > c1 and count < c2):
                            video_writer.write(frame)
                        if (count == c2):
                            break
                        count = count + 1
                    video_writer.release()
                    cap.release()

if __name__ == '__main__':
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    find(1688451070, "test", fourcc, 25, 1280, 720)

