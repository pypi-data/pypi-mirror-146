import cv2
import matplotlib.pyplot as plt


def show_img(img):
    """
    img: str/numpy array
    """
    if type(img) == str:
        img = cv2.imread(img)
    elif type(img) == numpy.ndarray:
        pass
    else:
        raise TypeError("img is either a str or numpy array")
    plt.imshow(img[:,:,::-1])
    plt.show()


def show_hist(data, bins=20, range=None, color="blue", edgecolor="black", alpha=0.7, normed=0, **kwargs):
    """
    data: data to show hist, list
    bins: bin+1 edges / half-open edges/ binning strategy, 20, int/list/str
    range: lower and upper range of the bins, tuple/None
    color: bar color, blue, str
    edgecolor: bar edge color, black, str
    alpha: alpha, 0.7, float
    others: ......
    """
    plt.hist(data, bins, range, normed=normed, facecolor=color, edgecolor=edgecolor, alpha=alpha, **kwargs)

