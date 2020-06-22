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

    # old pattern that didn't check for puzzle key to sort"""
    # pattern = re.compile(r"(?P<tail>\S+\/[a-z]\S+)")

    # new pattern below to try to test animal or place
    p = re.compile(
        r"(?P<tail>\S+\/[a-z]\S+(?P<puzzle_key>\/\w-\w+-\w+|\/\w-\w+).\w+)")
    head = "http://code.google.com"
    with open(filename)as f:
        result = (f.read().splitlines())
    # print(result[3])
    print(result[0])
    print(p.search(result[1]).group("puzzle_key")[-4:])
    # print(pattern.search(result[0]).group("tail"))
    # print(pattern.search(test)[0])
    # print("puzzle" in result[0])

    # testing puzzle keys
    # keys = ["/p-bjab-bbih", "/a-aaaa"]
    # a_key, p_key = keys
    # print(sorted(keys, key=lambda key: key[-4:]))

    #####
    # print(sorted(result, key=lambda p_key: p_key= p_key= p.search(
    #     p_key).group("puzzle_key")[-4:]))

    puzzle_pieces = {head+match.group("tail")
                     for piece in result
                     if (match := p.search(piece))
                     and "puzzle" in piece}
    # print(puzzle_pieces)
    # print(sorted(puzzle_pieces))
    return sorted(puzzle_pieces, key=lambda p_key: p_key[-8:-4])


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
        os.mkdir((os.path.join(directory)))

    except FileExistsError as error:
        print(f"{error=}")

    finally:
        print("done =)")
    print("downloading images ....")
    for index, image in enumerate(img_urls):
        urllib.request.urlretrieve(
            image, filename=os.path.join(directory, f"img{index}.jpg"))
    print("finished")

    with os.scandir(directory) as d:
        files = sorted([f.name for f in d],
                       key=lambda string: int(string[3:-4]))
        # print(files)
        # print(sorted(files, key=lambda string: int(string[3:-4])))
    img_tags = [f"<img src={os.path.relpath(f)}>" for f in files]

    html = f"""
<html>
<body>
{"".join(img_tags)}
</body>
</html>"""

    index_html = os.path.join(directory, "index.html")
    with open(index_html, "w") as index:
        index.write(html)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main():
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()
    parsed_args = parser.parse_args()

    if not parsed_args:
        parser.print_usage()
        sys.exit(1)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
