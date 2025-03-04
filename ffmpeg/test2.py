import subprocess
import time

def start_stream(input_url, output_url):
    # command = ['ffmpeg', "-re", "-i", input_url, "-vcodec", "copy", '-c:a', 'aac', '-ar', '44100', "-f", "flv", output_url]
    # command = ['ffmpeg', '-re', '-i', input_url, '-vcodec', 'copy', '-rtsp_transport', 'tcp', '-f', 'rtsp', output_url]
    command = ['ffmpeg', '-rtsp_transport', 'tcp', '-i', input_url, '-vcodec', 'libx264', '-an', '-f', 'flv', output_url]
    # command = ["ffmpeg", "-re", "-i", input_url, "-vcodec", "libx264", "-an", "-f", output_url]
    print(command)
    process = subprocess.Popen(command)
    return process

def stop_stream(process):
    process.terminate()
    process.wait()

input_url = "rtsp://192.168.1.150:8557/h264"
output_url = "rtmp://118.190.156.22:1935/live/1"
# http://118.190.156.22/flv_live?port=1935&app=live&stream=1

if __name__ == "__main__":
    stream_process = start_stream(input_url, output_url)
    time.sleep(300)
    stop_stream(stream_process)
    pass
