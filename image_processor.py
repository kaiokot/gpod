
import logging
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import logging
import os
from datetime import datetime
import pytz
from os import path
from os.path import isdir


class AzureComputerVision():
    def __init__(self, setting):
        self.setting = setting

    def describe(self, image_url):
        logger = logging.getLogger("gpod")

        try:
            if image_url is None:
                raise ValueError("image_url")

            computervision_client = ComputerVisionClient(
                self.setting["azure"]["endpoint"], CognitiveServicesCredentials(self.setting["azure"]["subscription_key"]))

            max_descriptions = 3

            analysis = computervision_client.describe_image_in_stream(
                image_url, max_descriptions, "en")

            logger.info(analysis)

            return {
                "captions": list(map(lambda a: (a.text, a.confidence), analysis.captions)),
                "tags": analysis.tags
            }
        except Exception as ex:
            logger.error("Error: {}".format(ex))
            raise ex


class TimeLapse():
    def __init__(self, settings):
        self.settings = settings

    def create(self):
        logger = logging.getLogger("gpod")

        try:
            logger.info("starting to create TimeLapse...")

            now = datetime.now(pytz.timezone(
                self.settings["time"]["zone"]))

            images_path = path.join("images", self.settings["id"])

            dest_path = path.join(images_path, "timelapse")

            dest_file = path.join(dest_path, "{}.mov".format(
                self.settings["id"]))

            dest_file_sound = path.join(dest_path, "{}.mov".format(
                self.settings["id"] + "_sound"))

            resolution = "{}x{}".format(
                self.settings["width"], self.settings["height"])

            if not isdir(dest_path):
                os.makedirs(dest_path)

            os.system("ffmpeg -y -framerate 5 -pattern_type glob -i '{}/*.jpeg' -s:v {} -c:v prores -profile:v 3 -pix_fmt yuv422p10 {} -loglevel error".format(
                images_path, resolution, dest_file))

            logger.info(
                self.settings["id"] + " - create video TimeLapse...!")

            os.system("ffmpeg -y -i {} -i piano.mp3 -map 0 -map 1:a -c:v copy -shortest {} -loglevel error".format(
                dest_file, dest_file_sound))

            logger.info(
                self.settings["id"] + " - create video with sound TimeLapse...!")

            logger.info(
                self.settings["id"] + " - success on create TimeLapse...! {}".format(dest_file_sound))

            return dest_file_sound, now

        except Exception as ex:
            logger.error("Error: {}".format(ex))
            raise ex
