from collections import defaultdict
from pathlib import Path


def get_paths(paths: list[str], recursive: bool) -> defaultdict[str, list[Path]]:
    """
    Get all the XMP files from the list of paths given in the arguments.
    Usually expects folders, but can also add single files if they match the "*.xmp" pattern.

    :param paths: List of paths to get the files from.
    :param recursive: Whether to get the files recursively or not.
    :return: A dictionary containing the file names as keys and list of paths as values.
    """
    files = defaultdict(list)
    pattern = "*.xmp"
    for path in paths:
        path = Path(path)
        if path.is_dir():
            # Use rglob if recursive, glob otherwise.
            # Could also change pattern to "**/*.xmp" if recursive and give to glob.
            glob_strategy = path.rglob if recursive else path.glob
            for file in glob_strategy(pattern):
                if file.is_file():
                    files[file.name].append(file)

        elif path.is_file() and path.match(pattern):
            files[path.name].append(path)
    return files
