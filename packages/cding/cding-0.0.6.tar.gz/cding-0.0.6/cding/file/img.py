import cv2


def imread(filename, flag=1):
    """
    filename: str
    flag: 1: color without alpha, 0: grey mode, -1: unchanged with alpha
    """
    img = cv2.imread(filename, flag)
    if img is None:
        raise ValueError("image dir not found")
    else:
        return img


def imwrite(filename, img):
    """
    filename: str
    img: img to save
    """
    if img is None:
        raise ValueError("image is empty")
    else:
        return cv2.imwrite(filename, img)

