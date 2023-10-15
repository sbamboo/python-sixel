#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
import argparse
from sixel import converter


def main():
    parser = argparse.ArgumentParser(prog='PySixel converter example')

    parser.add_argument('image_path', type=Path)
    args = parser.parse_args()

    if not args.image_path.exists():
        logging.error(f"Path '{args.image_path}' does not exist.")
        return

    sixel_converter = converter.SixelConverter(args.image_path)
    sixel_converter.write(sys.stdout)


if __name__ == "__main__":
    main()
