#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# RegexMate: A Visual Regular Expression Test/Evaluation tool
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 29th June 2013
#
# Licensed under MIT license. Refer COPYING for more info.


import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import widgets
from regex import *


__version__ = (0, 9, 0)
__author__ = 'Sreejith Kesavan'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2013 Sreejith Kesavan'


class RegexMate(QDialog):
    """Main widget for the application"""

    def __init__(self, parent=None):
        super(RegexMate, self).__init__(parent)
        # handle all the Regular Expression stuff
        self._validator = RegexValidator()

        # create layout and add widgets
        self.layout = QVBoxLayout()
        self._regex_form = self.create_regex_form()
        self._text_area = self.create_input_sheet()

        # setup signals and slots
        self._regex_form.regexChanged.connect(self._text_area.highlight_matches)

        self.layout.addWidget(self._regex_form)
        self.layout.addWidget(self._text_area)
        self.setLayout(self.layout)
        # set the window size
        self.resize(800, 600)

        self.setWindowTitle('RegexMate (v%s)' % '.'.join(map(str, __version__)))

    def create_regex_form(self):
        """Create appropriate widgets to enter the regex and supported
        parameters"""
        return widgets.RegexForm(self, self._validator)

    def create_input_sheet(self):
        """Create the widgets needed to display the text to be validated.
        Matches are also highlighted in this field."""
        return widgets.TextArea(self, self._validator)


def start():
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/icon.png')
    app.setWindowIcon(QIcon(icon_path))
    regexmate = RegexMate()
    regexmate.show()
    app.exec_()


if __name__ == '__main__':
    start()
