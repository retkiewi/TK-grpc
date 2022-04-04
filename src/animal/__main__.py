import os
from itertools import groupby
from operator import itemgetter

from detecto import core, utils


file_path = "\\elephant.jpg"
model_path = "\\model_weights.pth"

dir_path = os.path.dirname(os.path.realpath(__file__))

model_path = dir_path + model_path
file_path = dir_path + file_path

model = core.Model.load(model_path, ['tiger', 'elephant', 'panda'])
image = utils.read_image(file_path)

predictions = model.predict(image)

labels, _, scores = predictions

animal_score = list(zip(labels, list(map(lambda x: float(x), scores))))

first = itemgetter(0)
scores_maximum = [(k, max(item[1] for item in tups_to_sum))
        for k, tups_to_sum in groupby(sorted(animal_score, key=first), key=first)]

scores_maximum = list(map(lambda x: (x[0], round(x[1] * 100, 2)), scores_maximum))

print(scores_maximum)
