#! /usr/bin/env python
# -*- coding: utf-8 -*-


import re
import functools
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RegexForm(QWidget):
    """A Text Editor widget to enter the Regular Expression
    and choose appropriate options.

    This class basically acts as a widget container that actually
    packs a QTextEdit field to enter the Regular Expression and a
    QCheckBox widget to choose Regular Expression flags.
    """

    def __init__(self, parent=None, validator=None):
        super(RegexForm, self).__init__(parent)
        self._parent = parent
        self._validator = validator

        # create the regex input widget and the options widget
        self.create_text_widget()
        self.create_options_widget()

    def create_text_widget(self):
        """Create the text widget"""
        self.text_widget = QTextEdit(self)
        self.text_widget.setFixedHeight(50)

        # recompile the regex with the new pattern, if changed
        self.text_widget.textChanged.connect(self._recompile_regex)

        # we set the layout to the parent layout to align all widgets
        # in the same vertical line
        self._parent.layout.addWidget(self.text_widget)

    def create_options_widget(self):
        """Widgets to select the regex options"""
        options_box = QGroupBox('Regex Flags')
        flags_layout = QHBoxLayout()

        # Check boxes that represent re flags
        re_case = QCheckBox('Case Insensitive')
        re_dotall = QCheckBox('Dot (.) matches all')
        re_multiline = QCheckBox('^$ matches at line breaks')
        flags_layout.addWidget(re_case)
        flags_layout.addWidget(re_dotall)
        flags_layout.addWidget(re_multiline)
        options_box.setLayout(flags_layout)

        # Setup callbacks on checkbox update
        re_case.stateChanged.connect(
            functools.partial(self._update_regex_flags, re.IGNORECASE))

        re_dotall.stateChanged.connect(
            functools.partial(self._update_regex_flags, re.DOTALL))

        re_multiline.stateChanged.connect(
            functools.partial(self._update_regex_flags, re.MULTILINE))

        self._parent.layout.addWidget(options_box)

    def _update_regex_flags(self, flag, state):
        """Update the regex flags if options are changed

        Arguments:
        - `flag`: The regex flag
        - `state`: The state of the flag, either checked or unchecked (boolean)
        """
        state = (state == Qt.Checked)
        self._validator.update_flags(flag, state)

    def _recompile_regex(self):
        """Recompiles the Regular expression with the new pattern."""
        pattern = str(self.text_widget.toPlainText())
        self._validator.update_regex(pattern)


class TextArea(QPlainTextEdit):
    """A Text Editor widget to enter the text data"""

    # colors to represent regex match groups
    GROUP_COLORS = [
        Qt.yellow, Qt.blue, Qt.green
        ]

    def __init__(self, parent=None, validator=None):
        super(TextArea, self).__init__(parent)
        self._validator = validator
        # Re-compile the regex if the pattern changes
        self.textChanged.connect(self._highlight_matches)

    def _highlight_matches(self):
        """Highlight matches in the text against the pattern."""

        # The input text to be highlighted against the regex match
        text = str(self.toPlainText())
        # update the regex validator
        self._validator.update_text(text)

        for match in self._validator.find_matches():
            # identify the number of matched groups from this text
            groups = match.groups()
            num_groups = len(groups)
            if num_groups == 0:
                # if there are no groups, find the default group
                groups = (match.group(0), )
                num_groups = 1

            # pick different colors for each group
            colors = self._pick_colors(num_groups)
            # highlight groups using the chosen colors
            for text, color in zip(groups, colors):
                self._highlight(text, color)

    def _pick_colors(self, num):
        """Returns `num` different colors for highlighting groups

        Arguments:
        - `num`: number of colors to return
        """
        return self.GROUP_COLORS[:num]

    def _highlight(self, text, color):
        """Highlight the text with the given color

        Arguments:
        - `text`: text snippet to be highlighted
        - `color`: the highlight color
        """
        print 'Highlight %s with color %r' % (text, color)
        fmt = QTextCharFormat()
        fmt.setBackground(color)

        ## cursor = QTextCursor(self.document())
        ## cursor.setPosition(begin, QTextCursor.MoveAnchor)
        ## cursor.setPosition(end, QTextCursor.KeepAnchor)
        ## cursor.setCharFormat(fmt)

        cursor = self.document().find(text)
        if cursor:
            cursor.setCharFormat(fmt)
