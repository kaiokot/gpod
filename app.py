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
subscription_key = "subscription_key"
endpoint = "endpoint"


class CameraWorker(Thread):
    def __init__(self, settings, queue):
        Thread.__init__(self)
        self.settings = settings
        self.queue = queue

    def run(self):
        try:
            while True:
                prev = Preview(self.settings["preview"])
                cam = None
                print("working on {} ......".format(self.settings["id"]))
                type = self.settings["type"]
                input_address = self.settings["input_address"]

                
                print("using local camera time self.settings...")
                setting_time_zone = self.settings["time"]["zone"]
                setting_time_start = self.settings["time"]["start"]
                setting_time_end = self.settings["time"]["end"]
                setting_interval_secs = self.settings["time"]["interval_seconds"]

                hour = datetime.now(
                    pytz.timezone(setting_time_zone)).hour

                if (setting_time_start <= hour <= setting_time_end):

                    if(type == "usb"):
                        cam = UsbCam()
                    elif(type == "rtsp"):
                        cam = RtspCam(input_address)
                    else:
                        print("invalid cam type...")

                    print("starting to process image...")

                    cam.take()
                    print("success on take pic!")

                    list_of_files = glob.glob('images/*.jpeg')
                    latest_file = max(list_of_files, key=os.path.getctime)
                    print("success on get last pic!")

                    filepath = open(latest_file, 'rb')
                    azure_cv = AzureComputerVision(subscription_key, endpoint)
                    result = azure_cv.describe(filepath)
                    print("success on describe pic!")

                    with open(latest_file + ".json", 'w') as outfile:
                        json.dump(result, outfile)
                    print("success on save description json  to pic!")

                    # # send preview
                    # prev.check_directory()
                    # dest_path = self.settings["preview"]["git_dir"]
                    # dest_pic = dest_path + "/photo.jpeg"
                    # dest_json = dest_path + "/description.json"

                    # shutil.copyfile(latest_file, dest_pic)
                    # shutil.copyfile(latest_file + ".json", dest_json)
                    # print("success on copy files to git dir!")

                    # prev.publish()
                    # print("success on publish to github!")

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

        for setting in settings["cameras"]:
            worker = CameraWorker(setting, queue)
            # worker.daemon = True
            worker.start()

        queue.join()

    except Exception as ex:
        print(ex)
   
if __name__ == "__main__":
    main()