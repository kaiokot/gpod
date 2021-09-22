from preview import Preview
import time
from camera import UsbCam
from image_processor import AzureComputerVision
import glob
import os
import json
import sys
import shutil


subscription_key = "subscription_key"
endpoint = "endpoint"

if __name__ == "__main__":

    try:
        config = {}
        try:
            with open("configs/settings.json") as f:
                config = json.loads(f.read())
        except Exception as e:
            sys.stderr.write("Error: {}".format(e))
            sys.exit(1)

        cam = UsbCam()
        prev = Preview(config["preview"])

        while True:
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

            # send preview
            prev.check_directory()
            dest_path = config["preview"]["git_dir"]
            dest_pic = dest_path + "/photo.jpeg"
            dest_json = dest_path + "/description.json"

            shutil.copyfile(latest_file, dest_pic)
            shutil.copyfile(latest_file + ".json", dest_json)
            print("success on copy files to git dir!")

            prev.publish()
            print("success on publish to github!")

            print("everything is alright! \n")

            time.sleep(60)
    except Exception as ex:
        print(ex)
