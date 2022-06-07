import json
import cv2
from random import randrange
from Utils.Utils import get_comparator


def findFaces(path):
    img = cv2.imread(path)
    trained_face_data = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert to grayscale
    grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img)

    return len(face_coordinates)


def findSmiles(path):
    img = cv2.imread(path)
    number_of_smiles = 0
    # Load some pre-trained data on face frontals from opencv (haar cascade algorithm)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

    # Convert to grayscale
    grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_detector.detectMultiScale(grayscaled_img)

    # Run the face detector within each of these faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (100, 200, 50), 4)

        # Get the sub frame (using numpy N-diminsional array slicing)
        the_face = img[y:y + h, x:x + w]

        # Change to grayscale
        face_grayscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)

        # Detects smiles
        smiles = smile_detector.detectMultiScale(
            face_grayscale, scaleFactor=1.7, minNeighbors=20)  # scaleFactors,min_neighbours

        number_of_smiles += len(smiles)
    return number_of_smiles


def get_filter_and_reference(filter_type, faces, smiles):
    return {"faces": (findFaces, [faces]),
            "smiles": (findSmiles, [smiles]),
            "faces&smiles": (lambda path: [findFaces(path), findSmiles(path)], [faces, smiles])
            }[filter_type]


def process_request(body: str):
    body = json.loads(body)
    params = body["params"]
    paths = body["paths"]

    smiles = params["no smiles"]
    faces = params["no faces"]
    filter_method, references = get_filter_and_reference(params["type"], faces, smiles)

    threshold = float(params['threshold']) if 'threshold' in params else 0
    comparator = get_comparator(params["comparator"], threshold)
    print(params["comparator"])

    return [*filter(lambda path: is_compliant(path, filter_method, comparator, references), paths)]


def is_compliant(path, filter_method, comparator, references):
    val = filter_method(path)
    values = val if isinstance(val, list) else [val]
    refs = [float(reference) if isinstance(reference, str) else reference for reference in references]
    return any(map(comparator, values, refs))


def process_single(query):
    filter_method, references = get_filter_and_reference(query.type, query.faces, query.smiles)
    comparator = get_comparator(query.comparator, query.threshold)
    print(query.comparator)
    return is_compliant(query.path, filter_method, comparator, references)
