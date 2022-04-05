import os
from pathlib import Path
from detecto import core, utils


module_path = Path('animal')

model_path = module_path / "model_weights.pth"
file_path = module_path / "elephant.jpg"

animals = [
    'tiger',
    'elephant',
    'panda'
    ]

model = core.Model.load(model_path, animals)
image = utils.read_image(str(file_path))

labels, _, scores = model.predict(image)

animal_scores = {label: [score for i, score in enumerate(scores)
                            if labels[i] == label] for label in set(labels)}

for label in animal_scores:
    result = float(max(animal_scores[label]))
    print(f'{label} {result}')

