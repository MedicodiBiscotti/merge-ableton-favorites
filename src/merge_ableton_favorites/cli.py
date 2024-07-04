import argparse
from pathlib import Path


def parse_args(args):
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
    parser.add_argument(
        "-n",
        "--dry-run",
        "--noop",
        action="store_true",
        help="Do not write any files, just show what would be done.",
    )

    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument(
        "--prompt",
        action="store_true",
        dest="prompt",
        help="Prompt to continue after warning without --force.",
    )
    prompt_group.add_argument(
        "--no-prompt",
        action="store_false",
        dest="prompt",
        help="Fail after warning without --force.",
    )

    exclude_group = parser.add_mutually_exclusive_group()
    exclude_group.add_argument(
        "--include-root",
        action="store_false",
        dest="exclude_root",
        help="Include files in the root folder when recursive.",
    )
    exclude_group.add_argument(
        "--exclude-root",
        action="store_true",
        dest="exclude_root",
        help="Exclude files in the root folder when recursive.",
    )

    parser.set_defaults(prompt=True, exclude_root=False)
    return parser.parse_args(args)
