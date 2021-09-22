import time
from camera import UsbCam
from image_processor import AzureComputerVision


subscription_key = "subscription_key"
endpoint = "endpoint"


if __name__ == "__main__":
    azure_cv = AzureComputerVision(subscription_key, endpoint)

    image_url = "https://lh3.googleusercontent.com/lbp4sdU_lq8jx3rBw_SEjkA6hiD7KCiHwEcNPr2k8IFtwPxvabkWIXuJrKv_aeqVG_LMnYbi2dremkHXJCb-DXqkJ3WNQuV9erUXQytK3zf8_BSDyJ2KvW3wO3dYaTLyD4l1ovhJZiaqDe9sSqmNzazicocIWASU8cOEdk6cWTDbKotNKvC90bnqiRhTlYrog3H7DI3_q_76PJ5xVTsU9VVMpEWLBYKZXtlyeYkLoDdn4G0-NeUjHiz5_kEiYSfsD1RSgiRhAbp1fQghS3ct_9vorI1CtnBqgMqUtUf9DhAsQfpGh6KLoI1cr65ibkwzGTZ8ydaE171GvFIHlVaeDJxG_93PUjZOy8vYOXbwNdNHfN-4rJI1JM-7aAdLqaZEl3MjpPyolObhBidSqYk-aIZHCMtJWayDqtVM5_ajS7aICdhkl89-k1eJ2B6CW4QrfFelIi2B9nuIGcDodD79z3znSMDIg8rOMbQRY_K1-oz5SEcqYmLQ3W9wcMUq9aDqngnZbqmfCpj2dbD-_giDEKaqlNuVFTrimqFBFR11aB75S04AvmGhzlqLc7ZSXf20sz3l8XS5r13t4WcAtmpp6iM2wGtjjxVfAuzX9Jj9s5hPhXR5C9lwRUVZv3aeoYBt-b0CzOkM4MUZ3gcXfi-cT3vLvrMw9c9m9d4LPnPcuUckj9PJlG2D7v4FNzEqbO66uikU8fXJA5rZQq-IOMGIxFQlXw=w875-h656-no?authuser=0"

    result = azure_cv.describe(image_url)
    
    print(result)

    cam = UsbCam()

    while True:
        cam.take()  
        time.sleep(30)
