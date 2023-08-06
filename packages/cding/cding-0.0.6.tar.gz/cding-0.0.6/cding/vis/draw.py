import cv2


def draw_rec(img, x, y, w, h, rgb=(255,0,0), thickness=2, **kwargs):
    """
    img: numpy array
    x, y, w, h: top-left point and w, h of the rectangle, int
    rgb: (255, 0, 0), list
    thickness: 2, int
    others: ...
    """
    draw = cv2.rectangle(img, (x, y), (x+w, y+h), rgb[::-1], thickness, **kwargs)
    return draw


def draw_text(img, text, x, y, rgb=(255,0,0), size=1.2, thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, **kwargs):
    """
    img: numpy array
    text: str
    x, y: top-left point of the text, int
    rgb: (255, 0, 0), list
    size: 1.2, float/int
    thickness: 2, int
    fontFace: cv2.FONT_HERSHEY_SIMPLEX
    others: ...
    """
    draw = cv2.putText(img, text, (x, y), fontFace, size, rgb[::-1], thickness, **kwargs)
    return draw


