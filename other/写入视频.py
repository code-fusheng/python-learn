import cv2
import os
import threading

def export():
    #视频源
    video = "rtsp://192.168.1.150:8557/h264"
    #读取视频流
    cap = cv2.VideoCapture(video)
    #获取视频流基础属性
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(w)
    print(h)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #新开线程写入视频
    t1 = threading.Thread(target = write(cap, fps,w,h))
    t1.start()

def write(cap, fps,w,h):
    import time
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    #切片时间
    time_frame = fps*60*5
    #切片标志位
    num = 0
    while True:
        #关闭条件
        while cap.isOpened():
            #读取视频流
            ret, frame = cap.read()
            #断开条件
            print(num)
            #从该时间点读取视频流
            if num == 0:
                #将该时间点变为文件名，文件夹精确到天
                ts = int(time.time())
                year = time.localtime(ts).tm_year
                month = time.localtime(ts).tm_mon
                day = time.localtime(ts).tm_mday
                outputpath = "./outputs/{}/{}/{}".format(year, month,day)
                if os.path.exists(outputpath):
                    pass
                else:
                    os.makedirs(outputpath)
                filename = str(ts) + ".avi"
                output = outputpath + "/" + filename
                #开启写入
                video_writer = cv2.VideoWriter(output, fourcc, fps, (w,h))
            #写入帧
            video_writer.write(frame)
            num  = num+1
            #到切片时间关闭写入，重新循环
            if num == time_frame :
                video_writer.release()
                num = 0
                break
    cv2.destroyAllWindows()
    cap.release()
 
if __name__ == '__main__':
    export()
