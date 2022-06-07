import os


def check_for_formats(file_path: str, desired_formats: list[str]) -> bool:
    _, ext = os.path.splitext(file_path)
    return ext in desired_formats