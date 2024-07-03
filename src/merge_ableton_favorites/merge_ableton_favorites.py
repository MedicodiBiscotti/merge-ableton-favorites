import argparse
from collections import defaultdict
from pathlib import Path


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


if __name__ == "__main__":
    # Situations where arguments don't really make sense:
    # - Only one source and not recursive.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Paths to search for XMP files. Can be folders or files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=".",
        help="Output folder to write to.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search recursively in the given paths.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite the output files if they already exist.",
    )
    args = parser.parse_args()
    print(args)
    pass
