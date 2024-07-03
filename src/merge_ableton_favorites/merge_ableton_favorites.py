import sys
from collections import defaultdict
from pathlib import Path

import cli


def get_paths(paths: list[str], recursive: bool) -> defaultdict[str, list[Path]]:
    """
    Get all the XMP files from the list of paths given in the arguments.
    Usually expects folders, but can also add single files if they match the "*.xmp" pattern.

    :param paths: List of paths to get the files from.
    :param recursive: Whether to get the files recursively or not.
    :return: A dictionary containing the file names as keys and list of paths as values.
    :raises FileNotFoundError: If a path does not exist or no XMP files are found in the given paths.
    :raises ValueError: If a single file is given but doesn't match the "*.xmp" pattern.
    """
    files = defaultdict(list)
    pattern = "*.xmp"
    for path in paths:
        path = Path(path)

        # Fail early if the path does not exist. User could supply a right and a wrong path.
        # We don't want the wrong path to be ignored silently and produce unexpected result.
        if not path.exists():
            raise FileNotFoundError(f"Path '{path}' does not exist.")

        if path.is_dir():
            # Use rglob if recursive, glob otherwise.
            # Could also change pattern to "**/*.xmp" if recursive and give to glob.
            glob_strategy = path.rglob if recursive else path.glob
            for file in glob_strategy(pattern):
                if file.is_file():
                    files[file.name].append(file)

        elif path.is_file():
            if not path.match(pattern):
                raise ValueError(
                    f"File '{path}' does not match the pattern '{pattern}'."
                )
            files[path.name].append(path)

    if not files:
        raise FileNotFoundError("No XMP files found in the given paths.")
    return files


def main(args=None):
    args = cli.parse_args(args)
    print(args)


if __name__ == "__main__":
    main(sys.argv[1:])
    pass
