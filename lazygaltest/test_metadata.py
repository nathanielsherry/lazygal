# coding=utf-8
# Lazygal, a lazy satic web gallery generator.
# Copyright (C) 2010 Alexandre Rossi <alexandre.rossi@gmail.com>
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


import unittest
import os
import codecs
from __init__ import LazygalTest
from lazygal import metadata
from lazygal.generators import Album
from lazygal.sourcetree import Directory
from lazygal import pyexiv2api as pyexiv2


class TestFileMetadata(LazygalTest):

    def setUp(self):
        super(TestFileMetadata, self).setUp()

        self.source_dir = self.get_working_path()
        album = Album(self.source_dir)
        self.album_root = Directory(self.source_dir, [], [], album)

    def create_file(self, path, contents):
        f = open(path, 'w')
        f.write(codecs.BOM_UTF8)
        f.write(contents.encode('utf-8'))
        f.close()

    def test_album_name(self):
        album_name = u'Album de <b>l\'école<b>'
        self.create_file(os.path.join(self.source_dir, 'album-name'),
                         album_name)

        md = metadata.DirectoryMetadata(self.album_root)
        self.assertEqual(md.get()['album_name'], album_name)

    def test_album_desc(self):
        album_desc = u'Allons voir la fête de l\'école tous ensemble'
        self.create_file(os.path.join(self.source_dir, 'album-description'),
                         album_desc)

        md = metadata.DirectoryMetadata(self.album_root)
        self.assertEqual(md.get()['album_description'], album_desc)

    def test_img_desc(self):
        img_path = self.add_img(self.source_dir, 'captioned_pic.jpg')

        # Set dumy comment which should be ignored.
        im = pyexiv2.ImageMetadata(img_path)
        im.read()
        im['Exif.Photo.UserComment'] = 'comment not to show'
        im.write()

        # Output real comment which should be chosen over the dummy comment.
        image_caption = u'Les élèves forment une ronde dans la <em>cour</em>.'
        self.create_file(os.path.join(self.source_dir, img_path + '.comment'),
                         image_caption)

        imgmd = metadata.ImageInfoTags(img_path)
        self.assertEqual(imgmd.get_comment(), image_caption)

    def test_album_picture(self):
        img_names = ('ontop.jpg', 'second.jpg', )
        for img_name in img_names:
            self.add_img(self.source_dir, img_name)
        self.create_file(os.path.join(self.source_dir, 'album-picture'),
                         '\n'.join(img_names))

        # Reload the directory now that the metadata file is present
        self.album_root = Directory(self.source_dir, [], [],
                                    self.album_root.album)

        self.assertEqual(img_names[0], self.album_root.album_picture)

    def test_comment_none(self):
        im_md = metadata.ImageInfoTags(self.get_sample_path('sample.jpg'))
        self.assertEqual(im_md.get_comment(), '')

    def test_image_description(self):
        sample = 'sample-image-description.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), 'test ImageDescription')

    def test_jpeg_comment(self):
        sample = 'sample-jpeg-comment.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), 'test jpeg comment')

    def test_jpeg_comment_unicode(self):
        sample = 'sample-jpeg-comment-unicode.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), u'test jpeg comment éù')

    def test_usercomment_ascii(self):
        sample = 'sample-usercomment-ascii.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), u'deja vu')

    def test_usercomment_unicode_le(self):
        sample = 'sample-usercomment-unicode-ii.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), u'unicode test éà')

    def test_usercomment_unicode_be(self):
        sample = 'sample-usercomment-unicode-mm.jpg'
        im_md = metadata.ImageInfoTags(self.get_sample_path(sample))

        self.assertEqual(im_md.get_comment(), u'unicode test : éàê')


if __name__ == '__main__':
    unittest.main()


# vim: ts=4 sw=4 expandtab