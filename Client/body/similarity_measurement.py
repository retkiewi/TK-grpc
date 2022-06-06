import cv2
import numpy as np


def read_img_from_dir(base_path_img, path_img2):
    image = cv2.imread(base_path_img)
    image2 = cv2.imread(path_img2)

    shape = image.shape[:2]
    image2 = cv2.resize(image2, shape)
    return find_by_knn(image, image2)


def find_by_knn(img, img2):
    #  The shorter the distance, the more similar the images look to each other.
    img, img2 = np.reshape(np.array(img), (1, -1)),  np.reshape(np.array(img2), (1, -1))
    dists = list(np.sqrt(np.sum((img2-img)**2, axis=1)))
    return dists

