#! /usr/bin/env python
# -*- coding: utf-8 -*-


import re
import functools
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from regexmate.regex import *


class RegexForm(QWidget):
    """A Text Editor widget to enter the Regular Expression
    and choose appropriate options"""

    def __init__(self, parent=None):
        super(RegexForm, self).__init__(parent)
        self._parent = parent
        self._validator = RegexValidator()
        self.create_text_widget()
        self.create_options_widget()

    def create_text_widget(self):
        """Create the text widget"""
        self.text_widget = QTextEdit(self)
        self.text_widget.setFixedHeight(50)
        self._parent.layout.addWidget(self.text_widget)

    def create_options_widget(self):
        """Widgets to select the regex options"""
        options_box = QGroupBox('Regex Flags')
        flags_layout = QHBoxLayout()

        # re flags
        re_case = QCheckBox('Case Insensitive')
        re_dotall = QCheckBox('Dot (.) matches all')
        re_multiline = QCheckBox('^$ matches at line breaks')
        flags_layout.addWidget(re_case)
        flags_layout.addWidget(re_dotall)
        flags_layout.addWidget(re_multiline)
        options_box.setLayout(flags_layout)

        # Setup callbacks on checkbox update
        re_case.stateChanged.connect(functools.partial(self._update_regex_flags, re.IGNORECASE))
        re_dotall.stateChanged.connect(functools.partial(self._update_regex_flags, re.DOTALL))
        re_multiline.stateChanged.connect(functools.partial(self._update_regex_flags, re.MULTILINE))

        self._parent.layout.addWidget(options_box)

    def _update_regex_flags(self, flag, state):
        """Update the regex flags if options are changed"""
        state = (state == Qt.Checked)
        self._validator.update_flags(flag, state)


class TextArea(QPlainTextEdit):
    """A Text Editor widget to enter the text data"""
    
    def __init__(self, parent=None):
        super(TextArea, self).__init__(parent)
