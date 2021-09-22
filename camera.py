import time
import os
import uuid

# http://manpages.ubuntu.com/manpages/bionic/man1/fswebcam.1.html

class UsbCam():
    def __init__(self):
        pass

    def take(self):
        os.system("fswebcam -c configs/fswebcam.conf")
