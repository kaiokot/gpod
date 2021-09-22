import time
from camera import UsbCam
from image_processor import AzureComputerVision
import glob
import os
import json


subscription_key = "subscription_key"
endpoint = "endpoint"


if __name__ == "__main__":
    try:
        cam = UsbCam()

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

            print("everything is alright! \n")

            time.sleep(60)
    except Exception as ex:
        print(ex)
        