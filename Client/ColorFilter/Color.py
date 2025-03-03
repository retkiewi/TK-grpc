from enum import Enum
from typing import Tuple, List
from colorsys import hsv_to_rgb

Color: Tuple[float, float, float] = tuple[float, float, float]


class ColorSystem(Enum):
    RGB = 1
    HSV = 2
    CMYK = 3


class ColorMetric(Enum):
    max = 1
    min = 2
    mean = 3
    median = 4
    rms = 5
    percentage = 6


class ColorParams:
    __CMYK_SCALE = 100
    __RGB_SCALE = 255

    def __init__(self,
                 system: ColorSystem,
                 color: Color,
                 metric: ColorMetric,
                 comparator: str,
                 threshold: float,
                 percent_threshold: float,
                 tolerance: float
                 ):
        self.system = system  # this field stays for consistency
        self.color = color
        self.metric = metric
        self.comparator = comparator
        self.threshold = threshold
        self.percent_threshold = percent_threshold
        self.tolerance = tolerance

    @staticmethod
    def from_object(obj: dict):
        system = ColorSystem[obj['system']]
        color = ColorParams.__to_rgb(system, obj['color'])
        metric = ColorMetric[obj['metric']]
        comparator = obj['comparator'] if 'comparator' in obj else ''
        threshold = float(obj['threshold']) if 'threshold' in obj else 0
        percent_threshold = float(obj['% threshold']) if '% threshold' in obj else 0
        tolerance = float(obj['pixel tolerance']) if 'pixel tolerance' in obj else 0
        return ColorParams(system, color, metric, comparator, threshold, percent_threshold, tolerance)

    @staticmethod
    def from_grpc(target):
        system = ColorSystem[target.system]
        color = ColorParams.__to_rgb(system, [*target.color])
        metric = ColorMetric[target.metric]
        comparator = target.comparator
        threshold = target.threshold
        percent_threshold = target.percent_threshold
        tolerance = target.tolerance
        return ColorParams(system, color, metric, comparator, threshold, percent_threshold, tolerance)


    # color_repr is either a list of 3 or 4 floats
    @staticmethod
    def __to_rgb(system: ColorSystem, color_repr: List[float]) -> Color:
        if system == ColorSystem.RGB:
            [r, g, b, a] = color_repr
            return Color((r, g, b))  # necessary cast to tuple of length 3
        if system == ColorSystem.HSV:
            [h, s, v, a] = map(lambda x: x / 255.0, color_repr)
            (r, g, b) = (float(i * 255) for i in hsv_to_rgb(h, s, v))
            return Color((r, g, b))
        if system == ColorSystem.CMYK:  # do not panic
            [c, m, y, k] = color_repr
            r = ColorParams.__RGB_SCALE * (1.0 - (c + k) / float(ColorParams.__CMYK_SCALE))
            g = ColorParams.__RGB_SCALE * (1.0 - (m + k) / float(ColorParams.__CMYK_SCALE))
            b = ColorParams.__RGB_SCALE * (1.0 - (y + k) / float(ColorParams.__CMYK_SCALE))
            return Color((r, g, b))

