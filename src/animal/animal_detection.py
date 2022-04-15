from pathlib import Path
from detecto import core, utils

from animal.animals import animals

module_path = Path('animal')

model_path = module_path / "model_weights.pth"


def detect_animals(file_path):
    model = core.Model.load(model_path, animals)
    image = utils.read_image(str(file_path))

    labels, _, scores = model.predict(image)

    animal_scores = {label: [score for i, score in enumerate(scores)
                             if labels[i] == label] for label in set(labels)}

    return {label: round(float(max(animal_scores[label])) * 100) for label in animal_scores}
