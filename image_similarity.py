# Modified from source: https://m.blog.naver.com/codinglab9807/222711897434
import cv2


def determine_similarity(control: any, test: any) -> float:
    """Determines the CORREL value of test, when compared against control.

    :param control: The histogram of the image to be compared against
    :param test:    The histogram of the image to compare
    :return:        The CORREL value of two histograms
    """
    return cv2.compareHist(control, test, 0)


def main():
    control = cv2.imread("test_images/mahiro_wave.jpg")
    test = cv2.imread("test_images/najimi_stare.jpg")
    for i in range(500):
        sim = determine_similarity(control, test)
    print(sim)


if __name__ == "__main__":
    main()
