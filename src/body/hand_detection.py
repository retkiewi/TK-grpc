import cv2
import mediapipe as mp


def hand_detection(path_file: str) -> int:
    img = cv2.imread(path_file)
    hands = mp.solutions.hands.Hands(static_image_mode=True,
                                     max_num_hands=2,
                                     model_complexity=1,
                                     min_detection_confidence=0.5,
                                     min_tracking_confidence=0.5)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return int(100 * results.multi_handedness[0].classification[0].score) if results.multi_handedness is not None else 0
