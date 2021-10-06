#!/bin/python3


import os
from queue import Queue
from preview import Preview
import time
from camera import RtspCam, UsbCam
from image_processor import AzureComputerVision, TimeLapse
import json
import sys
from datetime import datetime
import pytz
import threading
from threading import Thread
import json
import logging
import sys

threadLock = threading.Lock()
threads = []


class CameraWorker(Thread):
    def __init__(self, settings, cam_setting, queue):
        Thread.__init__(self)
        self.settings = settings
        self.cam_setting = cam_setting
        self.queue = queue

    def run(self):
        try:
            while True:
                threadLock.acquire()
                cam = None

                logging.info("==============================================================")
                logging.info("working on {} ...".format(
                    self.cam_setting["id"]))
                logging.info("==============================================================")

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
                        logging.info("invalid cam type...")
                        continue

                    # take and save pic
                    pic_taken_file, pic_file_name, date_pic = cam.take()

                    if(self.settings["azure"]["describe"]):

                        # describe image using azure cognitive services
                        azure_cv = AzureComputerVision(self.settings)
                        az_desc = azure_cv.describe(pic_taken_file)
                        logging.info(self.cam_setting["id"] +
                                     " - success on describe pic!")

                        # save azure describe into json file
                        with open(pic_file_name + ".json", 'w') as outfile:
                            json.dump(
                                {"desc": az_desc, "dt": str(date_pic)}, outfile)
                    else:
                        # just save time into json
                        with open(pic_file_name + ".json", 'w') as outfile:
                            json.dump(
                                {"dt": str(date_pic)}, outfile)

                    logging.info(
                        self.cam_setting["id"] + " - success on save description json  to pic!")

                    # time_lapse = TimeLapse(self.cam_setting)
                    # time_lapse.create()

                    if(self.settings["publish_preview"]):
                         # send preview to ghpages
                        prev = Preview(self.settings, self.cam_setting["preview"])
                        prev.check_directory()
                        prev.move_files(pic_file_name)                        
                        prev.publish()

                        logging.info(self.cam_setting["id"] +
                                     " - success on publish preview to github!")

                    logging.info("everything is alright! \n")
                else:
                    logging.info("out of time range")

                threadLock.release()

                time.sleep(setting_interval_secs)

        finally:
            self.queue.task_done()


def main():
    try:

        logging.basicConfig(filename='logs/gpod.log',
                            level=logging.INFO, format='%(asctime)s %(message)s')
        logging.getLogger("gpod")

        logging.info(os.getcwd())

        settings = {}
        try:
            with open("configs/gpod.json") as f:
                settings = json.loads(f.read())
        except Exception as ex:
            logging.error("Error: {}".format(ex))
            sys.exit(1)

        queue = Queue()

        for cam_setting in settings["cameras"]:
            worker = CameraWorker(settings, cam_setting, queue)
            worker.daemon = True
            worker.start()
            threads.append(worker)

        for t in threads:
            t.join()

        queue.join()

    except Exception as ex:
        logging.error("Error: {}".format(ex))
        sys.exit(1)


if __name__ == "__main__":
    main()
