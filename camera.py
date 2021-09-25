import os
from datetime import datetime
import pytz

# http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html


class UsbCam():
    def __init__(self, settings):
        self.settings = settings

    def take(self):
        try:
            print("starting to take pic...")

            now = datetime.now(pytz.timezone(
                self.settings["time"]["zone"]))

            file_path = "images/" + now.strftime('%Y%m%d-%H%M%S.%f') + ".jpeg"

            os.system("fswebcam -d {} -c configs/fswebcam.conf --save {} ".format(
                self.settings["input_address"], file_path))

            print(
                self.settings["id"] + " - success on take pic! {}".format(file_path))

            return open(file_path, 'rb'),  file_path, now

        except Exception as ex:
            print(ex)
            raise ex

# https://ffmpeg.org/


class RtspCam():
    def __init__(self, settings):
        self.settings = settings

    def take(self):
        try:
            print("starting to take pic...")

            now = datetime.now(pytz.timezone(
                self.settings["time"]["zone"]))

            file_path = "images/" + now.strftime('%Y%m%d-%H%M%S.%f') + ".jpeg"

            os.system(
                "ffmpeg -y -i {} -f image2 -vframes 1 -pix_fmt yuvj420p -strftime 1 '{}' -loglevel error -stats ".format(self.settings["input_address"], file_path))

            print(
                self.settings["id"] + " - success on take pic! {}".format(file_path))

            return open(file_path, 'rb'),  file_path, now
        except Exception as ex:
            print(ex)
            raise ex
