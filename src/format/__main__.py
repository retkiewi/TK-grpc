import os

from src.core.walker import DirWalker


def main():
    pass


def get_files_by_format(search_path: str, desired_formats: list[str], undesired_formats: list[str]) -> list[str]:
    results = []

    def check_file(filename: str):
        _, ext = os.path.splitext(filename)
        if ext not in undesired_formats:
            if len(desired_formats) == 0 or ext in desired_formats:
                results.append(filename)

    dir_walker = DirWalker(search_path, check_file)
    dir_walker.walk()
    return results


if __name__ == '__main__':
    main()
