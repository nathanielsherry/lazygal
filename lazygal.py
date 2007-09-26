#!/usr/bin/env python
#
# Lazygal, a lazy satic web gallery generator.
# Copyright (C) 2007 Alexandre Rossi <alexandre.rossi@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys, os
from optparse import OptionParser

from lazygal.lazygal import Album
import lazygal

usage = "usage: %prog [options] albumdir"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output-directory",
                  action="store", type="string",
                  dest="dest_dir", default=".",
                  help="Directory where web pages, slides and thumbs will be written (default is current directory).")
parser.add_option("-t", "--theme",
                  action="store", type="string",
                  dest="theme", default="default",
                  help="Theme name (looked up in theme directory) or theme full path.")
parser.add_option("", "--clean-destination",
                  action="store_true",
                  dest="clean_dest", default=False,
                  help="Clean destination directory of files that should not be there.")
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="show_version", default=False,
                  help="Display program version.")
parser.add_option("", "--check-all-dirs",
                  action="store_true",
                  dest="check_all_dirs", default=False,
                  help="Exhaustively go through all directories regardless of source modification time.")
parser.add_option("-s", "--image-size",
                  action="store", type="string",
                  dest="image_size", default="small=800x600,medium=1024x768",
                  help="Size of images, define as <name>=<x>x<y>,..., eg. small=800x600,medium=1024x768.")
parser.add_option("-T", "--thumbnail-size",
                  action="store", type="string",
                  dest="thumbnail_size", default="150x113",
                  help="Size of thumbnails, define as <x>x<y>, eg. 150x113.")
parser.add_option("-q", "--quality",
                  action="store", type="int",
                  dest="quality", default=85,
                  help="Quality of generated JPEG images (default is 85).")
(options, args) = parser.parse_args()

if options.show_version:
    print 'lazygal version %s' % lazygal.__version__
    sys.exit(0)

if len(args) != 1:
    parser.print_help()
    sys.exit("Bad command line.")

source_dir = args[0]
if not os.path.isdir(source_dir):
    sys.exit("Directory " + source_dir + " does not exist.")

sizes = []
size_defs = options.image_size.split(',')
for single_def in size_defs:
    name, string_size = single_def.split('=')
    x, y = string_size.split('x')
    sizes.append((name, (int(x), int(y))))

x, y = options.thumbnail_size.split('x')
thumbnail = (int(x), int(y))

album = Album(source_dir, thumbnail, sizes, quality=options.quality)
album.set_theme(options.theme)
album.generate(options.dest_dir, options.check_all_dirs, options.clean_dest)


# vim: ts=4 sw=4 expandtab
