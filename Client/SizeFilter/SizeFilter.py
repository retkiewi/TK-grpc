import os
import json
import imagesize
from Utils.Utils import get_comparator

INCH2CM = 0.393701


def get_disk_size(path):
    size_in_b = os.path.getsize(path)
    size_in_KB = size_in_b / 1024
    return [size_in_KB]


def get_pixel_size(path):
    return imagesize.get(path)


def get_cm_size(path):
    width, height = imagesize.get(path)
    widthDPI, heightDPI = imagesize.getDPI(path)
    print(width, height)
    print(widthDPI, heightDPI)
    return [width / widthDPI * INCH2CM, height / heightDPI * INCH2CM]


def get_metric(unit):
    return {"kb": get_disk_size,
            "pixels": get_pixel_size,
            "cm": get_cm_size
            }[unit]


def is_compliant(path, metric, comparator, reference):
    value = metric(path)
    ref = reference if isinstance(reference, list) else [float(reference)]
    print(f'Checked({value}) has type: {type(value)}')
    print(f'Reference({ref}) has type: {type(ref)}')
    return any(map(comparator, value, ref))


def process_request(body: str):
    body = json.loads(body)
    params = body["params"]
    paths = body['paths']

    metric = get_metric(params['unit'])
    threshold = float(params['threshold']) if 'threshold' in params else 0
    comparator = get_comparator(params['comparator'], threshold)
    reference = params[params['unit']]

    return [*filter(lambda path: is_compliant(path, metric, comparator, reference), paths)]


def process_single(query):
    metric = get_metric(query.unit)
    comparator = get_comparator(query.comparator, query.threshold)
    reference = query.values

    return is_compliant(query.path, metric, comparator, reference)
