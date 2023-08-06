import time


def get_format_time(format_time):
    """
    format_time: int
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(format_time//1000))

    