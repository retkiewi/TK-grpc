import cv2


def face_detection(path_file: str) -> int:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(path_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, _, level_weights = face_cascade.detectMultiScale3(gray, 1.1, 6, outputRejectLevels=True)
    return 100-1/max(level_weights) if level_weights else 0
