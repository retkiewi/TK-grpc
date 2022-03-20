import os


def main():
    pass


def check_for_formats(file_path: str, desired_formats: list[str], undesired_formats: list[str]) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext not in undesired_formats:
        return len(desired_formats) == 0 or ext in desired_formats


if __name__ == '__main__':
    main()
