import cv2
import os
import requests
import numpy as np
from requests.exceptions import InvalidSchema


def img_from_path(path):
    try:
        image = cv2.imread(os.path.normpath(path))
    except cv2.error:
        print(f"Error: No valid image path: {path}")
        return -1
    else:
        if image is not None:
            return image
        else:
            print(f"Error: Path {path} returned None!")
            return -1


def img_from_link(link):
    try:
        resp = requests.get(link, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except (InvalidSchema, requests.exceptions.ConnectionError):
        print(f"Error: No valid image link: {link}")
        return -1
    else:
        if image is not None:
            return image
        else:
            print(f"Error: Link {link} returned None!")
            return -1
