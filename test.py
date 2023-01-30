import os
import multiprocessing
from image_similarity import determine_similarity
import cv2


class PathAndHistogram:
    def __init__(self, path: str, cv2imread: any):
        hsv = cv2.cvtColor(cv2imread, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        self.path = path
        self.histogram = hist


similarity_check_format_filter = ("jpg", "jpeg", "png")
number_of_threads = os.cpu_count()
potentially_duplicate_files = []
THRESHOLD = 0.995


# Unused, as both files will be appended to result list
def bigger_file_of_two(path1: str, path2: str) -> str:
    """Returns the file path of the bigger file between the two given."""
    if os.path.getsize(path1) > os.path.getsize(path2):
        return path1
    else:
        return path2


def part_of_list(input_list: list[any], part: int, splits: int) -> list[any]:
    """Returns the nth 'slice' of a list from a total number of equal slices."""
    return input_list[len(input_list) * (part-1) // splits:len(input_list) * part // splits]


def similar_pictures(existing: list[PathAndHistogram], new_downloads: list[PathAndHistogram], ret, threadno=0)\
        -> None:
    """Appends similar picture paths to a global variable list."""
    caught_files = []
    processed = 0
    for index, new_file in enumerate(new_downloads):
        for idx_existing in range(index, len(existing)):
            if new_file.path != existing[idx_existing].path:
                correl = determine_similarity(new_file.histogram, existing[idx_existing].histogram)
                if correl > THRESHOLD:
                    print(correl)
                    caught_files.append([new_file.path, existing[idx_existing].path])
        processed += 1
        print(f"Thread {threadno}: Finished comparison of file {processed} of total {len(new_downloads)}.",
              f"({round(processed / len(new_downloads), 4) * 100}%)")
    ret[threadno] = caught_files


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    opened_existing_images = []
    for root, dirs, file in os.walk(os.getcwd()):
        for name in file:
            if name.endswith(similarity_check_format_filter) and name not in [f.path for f in opened_existing_images]:
                print(f"Loading {root}/{name}")
                opened_existing_images.append(PathAndHistogram(f"{root}/{name}", cv2.imread(f"{root}/{name}")))

    input("Done loading image histograms onto memory. Press Enter to begin comparisons.")

    processes = []
    for i in range(number_of_threads):
        p = multiprocessing.Process(target=similar_pictures,
                                    args=(opened_existing_images,
                                          part_of_list(opened_existing_images,
                                                       i+1,
                                                       number_of_threads),
                                          return_dict,
                                          i,))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(return_dict)

    # print(potentially_duplicate_files)
