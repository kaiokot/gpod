
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import time


class AzureComputerVision():
    def __init__(self, subscription_key, endpoint):
        self.subscription_key = subscription_key
        self.endpoint = endpoint

    def describe(self, image_url):

        if image_url is None:
            raise ValueError("image_url")

        computervision_client = ComputerVisionClient(
            self.endpoint, CognitiveServicesCredentials(self.subscription_key))

        max_descriptions = 3

        analysis = computervision_client.describe_image(
            image_url, max_descriptions, "en")

        return {
            "captions": list(map(lambda a: (a.text, a.confidence), analysis.captions)),
            "tags": analysis.tags
        }
