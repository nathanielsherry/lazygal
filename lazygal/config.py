# Lazygal, a lazy satic web gallery generator.
# Copyright (C) 2011 Alexandre Rossi <alexandre.rossi@gmail.com>
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
import sys
import ConfigParser


class BetterConfigParser(ConfigParser.RawConfigParser):

    def getint(self, section, option):
        try:
            if not self.getboolean(section, option):
                return False
            else:
                raise ValueError
        except (ValueError, AttributeError):
            return ConfigParser.RawConfigParser.getint(self, section, option)

    def getstr(self, section, option):
        try:
            if not self.getboolean(section, option):
                return False
            else:
                raise ValueError
        except (ValueError, AttributeError):
            return ConfigParser.RawConfigParser.get(self, section, option)

    def load(self, other_config, sections=None):
        '''
        Take another configuration object and overload values in this config
        object.
        '''
        all_sections = False
        if sections is None:
            sections = other_config.sections()
            all_sections = True

        for section in sections:
            if all_sections or other_config.has_section(section):
                if not self.has_section(section):
                    self.add_section(section)
                for option in other_config.options(section):
                    self.set(section, option, other_config.get(section, option))


USER_CONFIG_PATH = os.path.expanduser('~/.lazygal/config')


DEFAULT_CONFIG = BetterConfigParser()
DEFAULT_CONFIG.readfp(open(os.path.join(os.path.dirname(__file__),
                                        'defaults.conf')))


class LazygalConfigDeprecated(BaseException): pass


class LazygalConfig(BetterConfigParser):

    def __init__(self):
        BetterConfigParser.__init__(self)
        self.load(DEFAULT_CONFIG)

    def check_deprecation(self, config=None):
        if config is None: config = self

        if config.has_section('lazygal'):
            raise LazygalConfigDeprecated("'lazygal' section is deprecated")

    def read(self, filenames):
        conf = BetterConfigParser()
        conf.read(filenames)
        self.load(conf)
        self.check_deprecation()

    def load(self, other_config, sections=None):
        self.check_deprecation(other_config)
        BetterConfigParser.load(self, other_config, sections)


class LazygalWebgalConfig(LazygalConfig):

    def __init__(self, global_config):
        LazygalConfig.__init__(self)
        LazygalConfig.load(self, global_config)

    def load(self, other_config):
        LazygalConfig.load(self, other_config,
                           sections=('webgal', 'template-vars', ))


# vim: ts=4 sw=4 expandtab
