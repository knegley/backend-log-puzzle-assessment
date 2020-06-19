#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename: str, /) -> list:
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # +++your code here+++
    pattern = re.compile(r"(?P<tail>\S+/[a-z]\S+)")
    head = "http://code.google.com"
    with open(filename)as f:
        result = (f.read().splitlines())
    # print(result)
    # print(pattern.search(result[0]).group("tail"))
    # print(pattern.search(test)[0])
    # print("puzzle" in result[0])
    puzzle_pieces = {head+match.group("tail")
                     for piece in result
                     if (match := pattern.search(piece))
                     and "puzzle" in piece}
    # print(puzzle_pieces)
    # print(sorted(puzzle_pieces))
    return sorted(puzzle_pieces)


def download_images(img_urls: list, dest_dir: str, /) ->None:
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """

    # +++your code here+++

    # (head, tail) = os.path.split(os.getcwd())
    directory = (os.path.join(os.getcwd(), dest_dir))
    try:
        print("creating directory.....")
        # directory = (os.path.join(os.getcwd(), "imgs"))
        # os.mkdir(directory)
        os.mkdir((os.path.join(os.getcwd(), dest_dir)))

    except FileExistsError as error:
        print(f"{error=}")

    finally:
        print("done =)")
    print("downloading images ....")
    for index, image in enumerate(img_urls):
        urllib.request.urlretrieve(
            image, filename=os.path.join(directory, f"img{index}"))
    print("finished")


with os.scandir(os.getcwd()+"/testing") as d:
    files = [f.name for f in d]
    # print(files)
    print(sorted(files, key=lambda string: int(string[3:])))


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
