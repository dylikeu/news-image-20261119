#!/usr/bin/env python3
"""Copy the bundled front page into the output directory.

Entry program for make.fun's news-image-20261119 bounty. It takes no
input and uses no network: it only copies news.png to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when that is set),
so two runs always write identical bytes.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "news.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
