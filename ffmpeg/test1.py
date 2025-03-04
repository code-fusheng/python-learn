import subprocess
import time
from datetime import datetime, timedelta

# 视频文件存储


class video_save:
    time_duration = 10
    start_timestamp = int(time.time())
    end_timestamp = start_timestamp + time_duration
    filename = str(start_timestamp) + "_" + str(end_timestamp) + ".mp4"
    input_url = "rtsp://192.168.1.150:8557/h264"
    cmd = ['ffmpeg', '-i', input_url, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-t', '10', filename]
    subprocess.call(cmd)


if __name__ == "__main__":
    pass
