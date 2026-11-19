#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261119.

Writes the pre-rendered summary of the world's news of Thursday
19 November 2026 (news.png, in this repository) to /output/entry.png.

Deterministic: copies the same bytes on every run. No network, no
randomness, no model calls. Python 3.13 standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "news.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")


if __name__ == "__main__":
    main()
