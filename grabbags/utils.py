import os
import re
import logging

MODULE_NAME = "grabbags" if __name__ == "__main__" else __name__

LOGGER = logging.getLogger(MODULE_NAME)

SYSTEM_FILES = [
    ".DS_Store",
    "Thumbs.db",
    "Icon\r"
]

APPLE_DOUBLE_REGEX = re.compile(r"^\._.*$")


def is_system_file(file_path) -> bool:
    """Check if a given file is a system file

    This should be helpful for iterating over files and determine if a file in
    a packing can be removed.

    Note:
        Files that are identified as a system file are:

            * .DS_Store
            * Thumbs.db
            * `AppleDouble files <https://en.wikipedia.org/wiki/AppleSingle_and_AppleDouble_formats>`_
            * `Icon resource forks <https://superuser.com/questions/298785/icon-file-on-os-x-desktop/298798#298798>`_

    Returns:
        True if the file a system file,
        False if it's not

    """

    if os.path.isdir(file_path):
        return False

    root_path, filename = os.path.split(file_path)

    if filename in SYSTEM_FILES:
        return True

    res = APPLE_DOUBLE_REGEX.findall(filename)
    if len(res) > 0:
        return True

    return False


def remove_system_files(root) -> None:
    """
    Remove system nested within a directory. Files such as DS_Store & Thumbs.db

    Note:

        This function works recursively.

    Args:
        root: path to a folder

    """
    for root, dirs, files in os.walk(root):
        for file_ in files:
            full_path = os.path.join(root, file_)

            if is_system_file(full_path):
                LOGGER.warn("Removing {}".format(full_path))
                os.remove(full_path)
