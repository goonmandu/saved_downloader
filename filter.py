import os
import re
import shutil
from chunk_md5 import chunk_md5


def recursive_in(filter_list, string):
    for entry in filter_list:
        if entry.lower() in string.lower():
            return True
    return False


def is_smaller_than(filepath, size):
    return os.path.getsize(filepath) < size


root_dir = './downloaded'
core_files = [
    ".gitignore",
    "credentials.py",
    "LICENSE",
    "main.py",
    "README.md",
    "test.py",
    "__pycache__",
    ".git",
    ".idea",
    ".DS_Store"
    "filter.py"
]

"""
Existing hash values.
Import existing hash values to temporary hash list.
Append hash values to temporary hash list as each file is scanned.
If the hash of the file is in the hash list, remove the file.

Pseudocode:
h = open(hashes)
hashes = [line.strip() for line in h.readlines()]
for file in files:
    hashes.append(md5hash(file))
    if md5hash(file) in hashes:
        os.remove(file)
hashes = set(hashes)

"""


def filter_dupes_and_invalids():
    print("Filtering duplicates and potentially invalid items...")
    to_move = []
    # Scan each file in ./downloaded, and append path+filename to to_move if "(digit)" is found within it
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            current_dir = os.path.join(subdir, file)
            if (is_smaller_than(current_dir, 4096) and not recursive_in(core_files, current_dir))\
                    or re.search(r"\(\d+?\)", current_dir) is not None:
                to_move.append(current_dir)

    # If to_move is empty,
    if not to_move:
        print("The filter caught nothing.")
    # If to_move is not empty,
    else:
        # Move each file in to_move to the filtered directory
        for path in to_move:
            shutil.move(path, f"filtered/{path.split('/')[-1]}")
            print(f"Filtered {path}.")

    print("Done.")

# DEBUG, comment out
# filter_dupes_and_invalids()
