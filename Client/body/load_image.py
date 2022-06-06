import cv2
import os
import requests
import numpy as np
from requests.exceptions import InvalidSchema
from typing import Optional


def img_from_path(path: str) -> Optional[np.ndarray]:
    try:
        image = cv2.imread(os.path.normpath(path))
    except cv2.error:
        print(f"Error: No valid image path: {path}")
        return None
    return image


def img_from_link(link: str) -> Optional[np.ndarray]:
    try:
        resp = requests.get(link, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except (InvalidSchema, requests.exceptions.ConnectionError):
        print(f"Error: No valid image link: {link}")
        return None
    return image
