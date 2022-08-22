import os
import re
import shutil


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


def filter_dupes_and_invalids():
    print("Filtering duplicates and potentially invalid items...")
    to_move = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            current_dir = os.path.join(subdir, file)
            if (is_smaller_than(current_dir, 4096) and not recursive_in(core_files, current_dir)) or re.search(r"\(\d+?\)", current_dir) is not None:
                to_move.append(current_dir)

    if not to_move:
        print("The filter caught nothing.")
    else:
        for path in to_move:
            shutil.move(path, f"filtered/{path.split('/')[-1]}")
            print(f"Filtered {path}.")

    print("Done.")

# DEBUG, comment out
# filter_dupes_and_invalids()
