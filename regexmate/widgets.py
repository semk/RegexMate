#! /usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RegexForm(QWidget):
    """A Text Editor widget to enter the Regular Expression
    and choose appropriate options"""
    
    def __init__(self, parent=None):
        super(RegexForm, self).__init__(parent)
        text_widget = self.create_text_widget()
        options_widget = self.create_options_widget()
        # use parent layout to align with other widgets
        parent.layout.addWidget(text_widget)
        parent.layout.addWidget(options_widget)

    def create_text_widget(self):
        """Create the text widget"""
        widget = QTextEdit(self)
        widget.setFixedHeight(50)
        return widget

    def create_options_widget(self):
        """Widgets to select the regex options"""
        options_box = QGroupBox('Regex Flags')
        flags_layout = QHBoxLayout()
        case_insensitive = QCheckBox('Case Insensitive')
        re_dotall = QCheckBox('Dot (.) matches all')
        re_multiline = QCheckBox('^$ matches at line breaks')
        flags_layout.addWidget(case_insensitive)
        flags_layout.addWidget(re_dotall)
        flags_layout.addWidget(re_multiline)
        options_box.setLayout(flags_layout)
        return options_box
        

class TextArea(QPlainTextEdit):
    """A Text Editor widget to enter the text data"""
    
    def __init__(self, parent=None):
        super(TextArea, self).__init__(parent)