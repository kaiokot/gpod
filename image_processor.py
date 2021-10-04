
import logging
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import time


class AzureComputerVision():
    def __init__(self, setting):
        self.setting = setting

    def describe(self, image_url):
        try:
            logger = logging.getLogger("gpod")
            
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
            logging.error("Error: {}".format(ex))
            raise ex
