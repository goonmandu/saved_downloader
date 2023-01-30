# Modified from source: https://m.blog.naver.com/codinglab9807/222711897434
import cv2
import numpy as np


# TODO: THIS FUNCTION DETECTS TOO MANY FALSE POSITIVES. FIND BETTER ALGORITHM.
def determine_similarity(control: any, test: any, method: any) -> float:
    """Determines the INTERSECT value of test, when compared against control.

    :param control: The histogram of the image to be compared against
    :param test:    The histogram of the image to compare
    :param method:  The cv2 HISTCMP method identifier of algorithm
    :return:        The CORREL value of two histograms
    """
    return cv2.compareHist(control, test, method)


def image_histogram(path: str):
    """Calculates the histogram from a given image path.

    :param path: The path string to target image.
    :return: The cv2 histogram object of image.
    """
    image = cv2.imread(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    return hist


def main():
    control = image_histogram("test_images/mahiro_wave_cropped.jpg")
    test = image_histogram("test_images/mahiro_wave_upscaled.jpg")
    for i in range(500):
        sim = determine_similarity(control, test)
    print(sim)


if __name__ == "__main__":
    main()
