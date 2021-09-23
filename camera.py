import time
import os
import uuid

# http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html


class UsbCam():
    def __init__(self):
        pass

    def take(self):
        os.system("fswebcam -c configs/fswebcam.conf")
        time.sleep(2)


class RtspCam():
    def __init__(self, ip_cam):
        self.ip_cam = ip_cam
        pass

    def take(self):
        os.system(
            "ffmpeg -y -i {} -f image2 -vframes 1 -pix_fmt yuvj420p -strftime 1 'images/%Y%m%d-%H%M%S.jpeg' -loglevel error -stats ".format(self.ip_cam))
        time.sleep(2)
