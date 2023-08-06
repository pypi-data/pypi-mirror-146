import os


def symlink(ori, dst):
    os.symlink(ori, dst)
    