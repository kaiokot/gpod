import time
import os
import uuid


class UsbCam():
    def __init__(self):
        pass

    def take(self):
        os.system("fswebcam ./images/"+str(uuid.uuid4())+".jpeg")
