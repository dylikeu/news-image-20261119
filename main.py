#!/usr/bin/env python3
"""Entrypoint: build news.png and copy it to the output directory.

Runs render.py (same directory) to draw the front page, then copies the
result to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
Stdlib only. Deterministic: same input files give byte-identical output.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "news.png")
    subprocess.run([sys.executable, os.path.join(HERE, "render.py")],
                   check=True)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
