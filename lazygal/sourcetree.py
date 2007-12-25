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

import os, sys, datetime, time
import Image

from lazygal import make, metadata


class File(make.FileSimpleDependency):

    def __init__(self, path, album):
        make.FileSimpleDependency.__init__(self, path)

        self.path = path
        self.album = album
        self.filename = os.path.basename(self.path)
        self.name, self.extension = os.path.splitext(self.filename)

    def _path_to_unicode(self, path):
        return path.decode(sys.getfilesystemencoding())

    def strip_root(self, path=None):
        found = False
        album_path = ""

        if not path:
            head = self.path
        else:
            head = path

        while not found:
            if head == self.album.source_dir:
                found = True
            elif head == "/":
                raise Exception("Root not found")
            else:
                head, tail = os.path.split(head)
                if album_path == "":
                    album_path = tail
                else:
                    album_path = os.path.join(tail, album_path)

        return album_path

    def rel_root(self):
        if os.path.isdir(self.path):
            cur_path = self.path
        else:
            cur_path = os.path.dirname(self.path)

        rel_root = ""

        while cur_path != self.album.source_dir:
            cur_path, tail = os.path.split(cur_path)
            rel_root = os.path.join('..', rel_root)
        return rel_root


class ImageFile(File):

    def __init__(self, path, album):
        File.__init__(self, path, album)
        self.exif = metadata.ExifTags(self.path)
        self.previous_image = None
        self.next_image = None

    def get_size(self, img_path=None):
        if not img_path:
            img_path = self.path
        im = Image.open(img_path)
        return im.size

    def get_date_taken(self):
        exif_date = self.exif.get_date()
        if exif_date:
            self.date_taken = exif_date
        else:
            # No date available in EXIF, or bad format, use file mtime
            self.date_taken = datetime.datetime.fromtimestamp(self.get_mtime())
        return self.date_taken

    def compare_date_taken(self, other_img):
        date1 = time.mktime(self.get_date_taken().timetuple())
        date2 = time.mktime(other_img.get_date_taken().timetuple())
        delta = date1 - date2
        return int(delta)


class Directory(File):

    def __init__(self, source, dirnames, filenames, album):
        File.__init__(self, self._path_to_unicode(source), album)

        self.dirnames = map(self._path_to_unicode, dirnames)
        self.dirnames.sort()
        self.filenames = map(self._path_to_unicode, filenames)

    def guess_directory_picture(self, subdir = None):
        '''
        Guesses picture for directory by finding first suitable image.
        '''
        directory = self.path
        relpath = ''

        if subdir is not None:
            directory = os.path.join(directory, subdir)
            relpath = subdir

        for root, dirs, files in os.walk(directory):
            subdirs = root[len(directory):]
            if len(subdirs) > 0 and subdirs[0] == '/':
                subdirs = subdirs[1:]
            for file in files:
                if self.album.is_ext_supported(file):
                    picture = os.path.join(relpath, subdirs, file)
                    return picture

        return None

    def is_album_root(self):
        return self.path == self._path_to_unicode(self.album.source_dir)


# vim: ts=4 sw=4 expandtab