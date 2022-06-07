from DogsFilter.lib.classifier import classifier
import json
import os


def run_classifier(path):

      # NOTE: this function only works for model architectures: 
      #      'vgg', 'alexnet', 'resnet'  
      model = "vgg"

      image_classification = classifier(path, model)
      return image_classification


def check_if_dog(path):
      filtered_paths = []
      with open(os.path.dirname(__file__) + "/lib/dognames.txt") as f:
            lines = f.read().splitlines() 
            classification = run_classifier(path).lower()
            if classification in lines:
                  return True
      return False


def check_breed(path, breed):
      filtered_paths = []
      classification = run_classifier(path)
      if breed in classification:
            return True
      return False

def get_filter(breed):
      if breed.lower() == "any":
            return lambda path, breed :check_if_dog(path)
      else: 
            return lambda path, breed :check_breed(path, breed)


def is_compliant(path, filter_method, breed):
      value = filter_method(path, breed)
      return value

def process_request(body):
      body = json.loads(body)
      params = body["params"]
      breed = params["breed"].lower()
      filter_method = get_filter(breed)
      paths=body["paths"]
      return [*filter(lambda path: is_compliant(path, filter_method, breed), paths)]



def process_single(query):
    breed = query.breed
    filter_method = get_filter(breed)
    path = query.path
    return is_compliant(path, filter_method, breed)