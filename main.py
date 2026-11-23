#!/usr/bin/env python3
"""Place the checked-in front page at /output/entry.png.

Stdlib only, no network, deterministic: the output bytes are the
checked-in image bytes, so repeated runs agree byte for byte.
"""
import os
import shutil
import sys


def bundled_image():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def destination(argv):
    if len(argv) > 1:
        return argv[1]
    return os.path.join(os.sep, "output", "entry.png")


def run(argv):
    target = destination(argv)
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(bundled_image(), target)
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))
