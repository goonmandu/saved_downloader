# Modified from source: https://m.blog.naver.com/codinglab9807/222711897434
import cv2


def determine_similarity(control: str, test: str) -> float:
    """Determines the CORREL value of test, when compared against control."""
    imgs = [cv2.imread(control), cv2.imread(test)]
    hists = []
    for img in imgs:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        hists.append(hist)
    query = hists[0]
    methods = ['CORREL']
    for index, name in enumerate(methods):
        for i, histogram in enumerate(hists):
            ret = cv2.compareHist(query, histogram, index)
    return ret


def main():
    control = "test_images/mahiro_wave.jpg"
    test = "test_images/najimi_stare.jpg"
    sim = determine_similarity(control, test)
    print(sim)


if __name__ == "__main__":
    main()
