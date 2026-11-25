#!/usr/bin/env python3
"""Sum up 25 November's world news in one image (news-image-20261125).

The entry image is baked into this repository as entry.png (drawn by the
authoring agent with Pillow in the build session). This program copies it
to /output/entry.png, the path the grader reads. Deterministic, no network,
standard library only.
"""
import hashlib
import os
import shutil
import struct
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

MAX_BYTES = 1048576
MAX_DIM = 1024


def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_gate(path):
    """Fail loudly if the output would be refused by the entry gate."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB gate" % size)
    width, height = png_dimensions(path)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 gate"
                         % (width, height))
    return size, width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = "/output/entry.png"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    if sha256_file(src) != sha256_file(dst):
        raise ValueError("copy to /output/entry.png failed integrity check")
    size, width, height = check_gate(dst)
    print("%s (%dx%d, %d bytes)" % (dst, width, height, size))


if __name__ == "__main__":
    sys.exit(main())
