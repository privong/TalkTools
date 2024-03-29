#!/usr/bin/env python
"""
Make a list of unique images files in a tex file, get list of images in
that directory, and print out which aren't being used in that tex file.
"""

import re
import sys
import os
import argparse


def main():
    """
    main routine
    """

    parser = argparse.ArgumentParser(description='Scan a TeX file and a directory \
to look for unused files. Optionally, suggest a renmaing of files to match \
figure order.')
    parser.add_argument('texfile', type=str, help='TeX file to scan.')
    parser.add_argument('--images', '-i', type=str, default='.',
                        help='Directory containing images.')
    """
    parser.add_argument('-r', '--reorder', action='store_true',
                        default=False, help='Suggest renaming of files to \
match order of figures in the file.')
    """
    args = parser.parse_args()

    suffix = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'eps', 'ps']

    if not args.images[-1] == '/':
        args.images = args.images + '/'

    try:
        texfile = open(args.texfile)
    except FileNotFoundError:
        sys.stderr.write("Error: couldn't open " + args.texfile +
" for reading.\n\n")
        sys.exit(1)

    imglist = []
    rmlist = []

    # get a list of all images included in the TeX file
    for line in texfile:
        if re.search('includegraphics', line):
            sline = line.split('\\includegraphics')
            for i in range(len(sline)-1):
                img = sline[i+1].split(']{')[1].split('}')[0]
                if not img in imglist:
                    imglist.append(img)

    for filename in os.listdir(args.images):
        nomatch = True
        i = 0
        while nomatch:
            if re.search(suffix[i], filename, re.IGNORECASE):
                nomatch = False
                if not (args.images + filename).split('\/')[-1] in imglist:
                    if not re.search(sys.argv[1].split('.tex')[0],
                                     (args.images + filename).split('\/')[-1]):
                        rmlist.append((args.images + filename).split('\/')[-1])
            i += 1
            if i >= len(suffix):
                break

    if imglist:
        imglist.sort()
        sys.stderr.write(str(len(imglist)) + " images found.\n")
        sys.stdout.write("Found images: ")
        for img in imglist:
            sys.stdout.write(img + ", ")
        sys.stdout.write("\n\n")
        """
        if args.reorder:
            sys.stdout.write("To rename figures to match order in text: \n")
            for i, img in enumerate(imglist):
                sys.stdout.write("\tmv " + img + " fig" + str(i) + "." +
                                 img.rsplit('.')[1] + "\n")
        """

    else:
        sys.stderr.write("Found no images to be included in TeX file.\n")
    if rmlist:
        sys.stdout.write("The unused images can be removed with this command:\n")
        sys.stdout.write("rm ")
        for img in rmlist:
            sys.stdout.write(img + ' ')
        sys.stdout.write("\n\n")
    else:
        sys.stderr.write("No unused images found.\n\n")

if __name__ == "__main__":
    main()
