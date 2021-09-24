import time
import os
import uuid
from datetime import datetime
import pytz
# http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html


class UsbCam():
    def __init__(self, cam_setting):
        self.cam_setting = cam_setting

    def take(self):
        now = datetime.now(pytz.timezone(
            self.cam_setting["time"]["zone"])).strftime('%Y%m%d-%H%M%S.%f')

        file_path = "images/" + now + ".jpeg"

        os.system("fswebcam -d {} -c configs/fswebcam.conf --save {} ".format(
            self.cam_setting["input_address"], file_path))

        return open(file_path, 'rb')


# https://ffmpeg.org/
class RtspCam():
    def __init__(self, cam_setting):
        self.cam_setting = cam_setting

    def take(self):
        now = datetime.now(pytz.timezone(
            self.cam_setting["time"]["zone"])).strftime('%Y%m%d-%H%M%S.%f')

        file_path = "images/" + now + ".jpeg"

        os.system(
            "ffmpeg -y -i {} -f image2 -vframes 1 -pix_fmt yuvj420p -strftime 1 '{}' -loglevel error -stats ".format(self.cam_setting["input_address"], file_path))

        return open(file_path, 'rb')
