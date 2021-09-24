from queue import Queue
from preview import Preview
import time
from camera import RtspCam, UsbCam
from image_processor import AzureComputerVision
import glob
import os
import json
import sys
import shutil
from datetime import datetime
import pytz
from threading import Thread

from os.path import isdir


subscription_key = "subscription_key"
endpoint = "endpoint"


class CameraWorker(Thread):
    def __init__(self, settings, queue, devices):
        Thread.__init__(self)
        self.settings = settings
        self.queue = queue
        self.devices = devices

    def run(self):
        try:
            while True:
                cam = None
                print("working on {} ......".format(self.settings["id"]))
                type = self.settings["type"]

                print("using local camera time settings...")

                setting_time_zone = self.settings["time"]["zone"]
                setting_time_start = self.settings["time"]["start"]
                setting_time_end = self.settings["time"]["end"]
                setting_interval_secs = self.settings["time"]["interval_seconds"]

                hour = datetime.now(
                    pytz.timezone(setting_time_zone)).hour

                if (setting_time_start <= hour <= setting_time_end):

                    if(type == "usb"):
                        cam = UsbCam(self.settings)
                    elif(type == "rtsp"):
                        cam = RtspCam(self.settings)
                    else:
                        print("invalid cam type...")
                        continue

                    print("starting to process image...")

                    pic_taken, pic_file_name, date_pic = cam.take()

                    print(
                        self.settings["id"] + " - success on take pic! {}".format(pic_file_name))

                    azure_cv = AzureComputerVision(subscription_key, endpoint)
                    result = azure_cv.describe(pic_taken)
                    print(self.settings["id"] +
                          " - success on describe pic!")

                    with open(pic_file_name + ".json", 'w') as outfile:
                        json.dump(
                            {"desc": result, "dt": str(date_pic)}, outfile)

                    print(
                        self.settings["id"] + " - success on save description json  to pic!")

                    # send preview
                    prev = Preview(self.settings["preview"])
                    prev.check_directory()

                    dest_path = self.settings["preview"]["git_dir"] + \
                        self.settings["preview"]["git_sub_dir"]

                    dest_pic = dest_path + "/photo.jpeg"
                    dest_json = dest_path + "/description.json"
                    dest_index_html = dest_path + "/index.html"

                    if not isdir(dest_path):
                        os.makedirs(dest_path)

                    with open(self.settings["preview"]["git_dir"] + "/devices.json", 'w') as outfile:
                        json.dump(self.devices, outfile)

                    shutil.copyfile(pic_file_name, dest_pic)
                    shutil.copyfile(pic_file_name + ".json", dest_json)
                    shutil.copyfile("index.html", dest_index_html)

                    print(self.settings["id"] +
                          " - success on copy files to git dir!")

                    prev.publish()
                    print(self.settings["id"] +
                          " - success on publish to github!")

                    print("everything is alright! \n")
                else:
                    print("out of time range")

                time.sleep(setting_interval_secs)
        finally:
            self.queue.task_done()


def main():
    try:
        settings = {}
        try:
            with open("configs/settings.json") as f:
                settings = json.loads(f.read())
        except Exception as e:
            sys.stderr.write("Error: {}".format(e))
            sys.exit(1)
        queue = Queue()

        devices = [item.get("id")for item in settings["cameras"]]

        for setting in settings["cameras"]:
            worker = CameraWorker(setting, queue, devices)
            # worker.daemon = True
            worker.start()

        queue.join()

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
