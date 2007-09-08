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

import os


__all__ = [
        'EXIF',
        'lazygal',
        ]

def get_darcs_lastdate():
    try:
        lazygal_dir = os.path.join(os.path.dirname(__file__), '..')
        inventory = os.path.join(lazygal_dir, '_darcs', 'inventory')
        sk = max(0, os.path.getsize(inventory)-200)
        inventoryf = open(inventory, 'r')
        inventoryf.seek(sk)
        last_lines = inventoryf.readlines()
        inventoryf.close()

        last_line = last_lines.pop()
        null, date_and_crap = last_line.split('**')
        return '+darcs' + date_and_crap[0:8]
    except IOError:
        return ''


__version__ = '0.0' + get_darcs_lastdate()

# vim: ts=4 sw=4 expandtab
