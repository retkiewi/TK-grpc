from enum import Enum


class ResultsPresentation(Enum):
    TOP_PICK = 0
    FIRST_PICK = 1
    ALL_FOUND = 2
    TOP_10 = 3
    TOP_20 = 4
    TOP_50 = 5


def get_name(result_presentation: ResultsPresentation):
    return result_presentation.name.lower().replace('_', ' ').capitalize()