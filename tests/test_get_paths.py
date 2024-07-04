import os

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from merge_ableton_favorites.merge_ableton_favorites import get_paths

# Imported for IntelliSense.
# pyfakefs doesn't work with C-based XML parsers like lxml.


def test_fakefs_works(fs: FakeFilesystem):
    # Arrange
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(file_name)

    # Assert
    assert os.path.exists(file_name)


def test_same_file_in_different_folders(fs: FakeFilesystem):
    # Arrange
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(f"a/{file_name}")
    fs.create_file(f"b/{file_name}")

    # Act
    pathdict = get_paths(["a", "b"], False)

    # Assert
    assert len(pathdict) == 1
    assert len(pathdict[file_name]) == 2


def test_same_file_in_different_folders_recursive(fs: FakeFilesystem):
    # Arrange
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(f"a/{file_name}")
    fs.create_file(f"b/{file_name}")

    # Act
    pathdict = get_paths(["."], True)

    # Assert
    assert len(pathdict) == 1
    assert len(pathdict[file_name]) == 2


def test_different_files_in_different_folders(fs: FakeFilesystem):
    # Arrange
    file_name1 = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    file_name2 = "57379c33-1601-52b3-9881-2f9dddeb963b.xmp"
    fs.create_file(f"a/{file_name1}")
    fs.create_file(f"b/{file_name2}")

    # Act
    pathdict = get_paths(["a", "b"], False)

    # Assert
    assert len(pathdict) == 2
    assert len(pathdict[file_name1]) == 1
    assert len(pathdict[file_name2]) == 1


def test_both_same_and_different_files_in_different_folders(fs: FakeFilesystem):
    # Arrange
    file_name1 = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    file_name2 = "57379c33-1601-52b3-9881-2f9dddeb963b.xmp"
    fs.create_file(f"a/{file_name1}")
    fs.create_file(f"b/{file_name1}")
    fs.create_file(f"b/{file_name2}")

    # Act
    pathdict = get_paths(["a", "b"], False)

    # Assert
    assert len(pathdict) == 2
    assert len(pathdict[file_name1]) == 2
    assert len(pathdict[file_name2]) == 1


def test_single_file(fs: FakeFilesystem):
    # Arrange
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(file_name)

    # Act
    pathdict = get_paths([file_name], False)

    # Assert
    assert len(pathdict) == 1
    assert len(pathdict[file_name]) == 1


def test_search_folder_and_single_file(fs: FakeFilesystem):
    # Arrange
    file_name1 = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    file_name2 = "57379c33-1601-52b3-9881-2f9dddeb963b.xmp"
    fs.create_file(f"a/{file_name1}")
    fs.create_file(file_name2)

    # Act
    pathdict = get_paths(["a", file_name2], False)

    # Assert
    assert len(pathdict) == 2
    assert len(pathdict[file_name1]) == 1
    assert len(pathdict[file_name2]) == 1


def test_given_no_paths_found_then_raise_error():
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        get_paths(["."], False)


def test_given_nested_file_without_recursive_then_raise_error(fs: FakeFilesystem):
    # Arrange
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(f"a/{file_name}")

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        get_paths(["."], False)


def test_given_nonexistent_file_then_raise_error(fs: FakeFilesystem):
    # Arrange
    file_name = "not-there.txt"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        get_paths([file_name], False)


def test_given_some_files_and_nonexistent_file_then_raise_error(fs: FakeFilesystem):
    # Arrange
    file_name1 = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    file_name2 = "not-there.txt"
    fs.create_file(file_name1)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        get_paths([file_name1, file_name2], False)


def test_given_wrong_filename_format_then_raise_error(fs: FakeFilesystem):
    # Arrange
    file_name = "wrong-name.txt"
    fs.create_file(file_name)

    # Act & Assert
    with pytest.raises(ValueError):
        get_paths([file_name], False)


def test_given_recursive_and_exclude_root_option_then_exclude_root(fs: FakeFilesystem):
    # Arrange
    file_name1 = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    file_name2 = "57379c33-1601-52b3-9881-2f9dddeb963b.xmp"
    fs.create_file(f"a/{file_name1}")
    fs.create_file(file_name2)

    # Act
    pathdict = get_paths(["."], True, True)

    # Assert
    assert len(pathdict) == 1
    assert len(pathdict[file_name1]) == 1
    assert file_name2 not in pathdict
