import os
from datetime import datetime
import pytz
from os import mkdir, path
from os.path import isdir

# http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html


class UsbCam():
    def __init__(self, settings):
        self.settings = settings

    def take(self):
        try:
            print("starting to take pic...")

            now = datetime.now(pytz.timezone(
                self.settings["time"]["zone"]))

            dest_path = path.join("images", self.settings["id"])
            file_path = path.join(dest_path, "{}.jpeg".format(
                now.strftime('%Y%m%d-%H%M%S.%f')))

            resolution = "{}x{}".format(
                self.settings["width"], self.settings["height"])

            if not isdir(dest_path):
                os.makedirs(dest_path)

            os.system("fswebcam -d {} --resolution '{}' -c configs/fswebcam.conf --save '{}' ".format(
                self.settings["input_address"], resolution, file_path))

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

            dest_path = path.join("images", self.settings["id"])
            file_path = path.join(dest_path, "{}.jpeg".format(
                now.strftime('%Y%m%d-%H%M%S.%f')))

            if not isdir(dest_path):
                os.makedirs(dest_path)

            resolution = "{}x{}".format(
                self.settings["width"], self.settings["height"])

            os.system(
                "ffmpeg -y -i {} -s '{}' -f image2 -vframes 1 -pix_fmt yuvj420p -strftime 1 '{}'  -loglevel error -stats ".format(self.settings["input_address"], resolution, file_path))

            print(
                self.settings["id"] + " - success on take pic! {}".format(file_path))

            return open(file_path, 'rb'),  file_path, now
        except Exception as ex:
            print(ex)
            raise ex
