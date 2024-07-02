import os

from pyfakefs.fake_filesystem import FakeFilesystem

# Imported for intellisense.
# pyfakefs doesn't work with C-based XML parsers like lxml.


def test_fakefs_works(fs: FakeFilesystem):
    file_name = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
    fs.create_file(file_name)
    assert os.path.exists(file_name)


def test_same_file_in_different_folders(fs: FakeFilesystem):
    pass


def test_same_file_in_different_folders_recursive(fs: FakeFilesystem):
    pass


def test_different_files_in_different_folders(fs: FakeFilesystem):
    pass


def test_both_same_and_different_files_in_different_folders(fs: FakeFilesystem):
    pass
