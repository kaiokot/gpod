import time
from camera import UsbCam
from image_processor import AzureComputerVision


subscription_key = "subscription_key"
endpoint = "endpoint"


if __name__ == "__main__":
    # azure_cv = AzureComputerVision(subscription_key, endpoint)

    # image_url = "image_url"

    # result = azure_cv.describe(image_url)
    
    # print(result)

    cam = UsbCam()

    while True:
        cam.take()  
        time.sleep(60)
