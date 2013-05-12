#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from regexmate import widgets


class RegexMate(QDialog):
    """Main widget for the application"""
    
    def __init__(self, parent=None):
        super(RegexMate, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.create_regex_form())
        self.layout.addWidget(self.create_input_sheet())
        self.setLayout(self.layout)
        # set the window size
        self.resize(800, 600)

    def create_regex_form(self):
        """Create appropriate widgets to enter the regex and supported
        parameters"""
        return widgets.RegexForm(self)

    def create_input_sheet(self):
        """Create the widgets needed to display the text to be validated.
        Matches are also highlighted in this field."""
        return widgets.TextArea(self)



def start():
    app = QApplication(sys.argv)
    regexmate = RegexMate()
    regexmate.show()
    app.exec_()


if __name__ == '__main__':
    start()
    