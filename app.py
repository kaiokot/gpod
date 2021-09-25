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

class CameraWorker(Thread):
    def __init__(self, settings, cam_setting, queue):
        Thread.__init__(self)
        self.settings = settings
        self.cam_setting = cam_setting
        self.queue = queue

    def run(self):
        try:
            while True:
                cam = None
                print("working on {} ......".format(self.cam_setting["id"]))

                setting_cam_type = self.cam_setting["type"]
                setting_time_zone = self.cam_setting["time"]["zone"]
                setting_time_start = self.cam_setting["time"]["start"]
                setting_time_end = self.cam_setting["time"]["end"]
                setting_interval_secs = self.cam_setting["time"]["interval_seconds"]

                hour = datetime.now(
                    pytz.timezone(setting_time_zone)).hour

                if (setting_time_start <= hour <= setting_time_end):

                    if(setting_cam_type == "usb"):
                        cam = UsbCam(self.cam_setting)
                    elif(setting_cam_type == "rtsp"):
                        cam = RtspCam(self.cam_setting)
                    else:
                        print("invalid cam type...")
                        continue

                    # take and save pic
                    pic_taken_file, pic_file_name, date_pic = cam.take()

                    # describe image using azure cognitive services
                    azure_cv = AzureComputerVision(self.settings)
                    az_desc = azure_cv.describe(pic_taken_file)
                    print(self.cam_setting["id"] +
                          " - success on describe pic!")

                    # save azure describe into json file
                    with open(pic_file_name + ".json", 'w') as outfile:
                        json.dump(
                            {"desc": az_desc, "dt": str(date_pic)}, outfile)
                    print(
                        self.cam_setting["id"] + " - success on save description json  to pic!")

                    # send preview
                    prev = Preview(self.settings, self.cam_setting["preview"])
                    prev.check_directory()
                    prev.move_files(pic_file_name)
                    prev.publish()
                    print(self.cam_setting["id"] +
                          " - success on publish preview to github!")

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

        for cam_setting in settings["cameras"]:
            worker = CameraWorker(settings, cam_setting, queue)
            # worker.daemon = True
            worker.start()

        queue.join()

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
