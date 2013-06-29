#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Qt Widgets for the main application. Includes the logic to
# highlight matches and groups dynamically
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 29th June 2013
#
# Licensed under MIT license. Refer COPYING for more info.


import re
import functools
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RegexForm(QWidget):
    """A Text Editor widget to enter the Regular Expression
    and choose appropriate options.

    This class basically acts as a widget container that actually
    packs a QTextEdit field to enter the Regular Expression and a
    QCheckBox widget to choose Regular Expression flags.
    """

    # This signal notifies any changes in the regex. This can be a change
    # in the regex pattern or the flags. Used for notifying the text widget
    # to update the highlights dynamically.
    regexChanged = pyqtSignal()

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

        # emit the change signal
        self.regexChanged.emit()

    def _recompile_regex(self):
        """Recompiles the Regular expression with the new pattern."""
        pattern = str(self.text_widget.toPlainText())
        self._validator.update_regex(pattern)

        # emit the change signal
        self.regexChanged.emit()


class TextArea(QPlainTextEdit):
    """A Text Editor widget to enter the text data"""

    def __init__(self, parent=None, validator=None):
        """Initialize the text widget. Setup the signals and the
        regex validator object.
        """
        super(TextArea, self).__init__(parent)
        # The regex validator
        self._validator = validator

        # List of colors to be used for regex matches and groups inside
        # each match. This will be dymically polulated once a regex
        # match is made.
        self._match_colors = []
        self._group_colors = []

        # Refresh the highlighting if the text changes
        self.textChanged.connect(self.highlight_matches)

    def highlight_matches(self):
        """Highlight matches in the text against the pattern.

        This method finds all the matches for the pattern in the text input
        and highlight all the matches with a unique color. Each group in a
        match is also given a unique color but it will be the same for all
        the matches.
        """

        # unhighlight first
        self._unhighlight()
        # The input text to be highlighted against the regex match
        text = str(self.toPlainText())
        # update the regex validator
        self._validator.update_text(text)

        for match_num, match in enumerate(self._validator.find_matches()):
            matched_text = match.group(0)

            # Choose a unique color for this match. Generate a new color
            # if there is no existing color for this match.
            try:
                color = self._match_colors[match_num]
            except IndexError:
                color = self._generate_random_color()
                self._match_colors.append(color)

            # Highlight the matched string. Tell the widget to highlight
            # the text using its start and end indices.
            self._highlight(match.start(), match.end(), color)

            # Find groups and highlight them too
            for group_num in range(len(match.groups())):
                group_text = match.group(group_num + 1)
                group_start_idx = match.start() + matched_text.find(group_text)
                group_end_idx = group_start_idx + len(group_text)

                # Choose a unique color for this group. Generate a new color
                # if there is no existing color for this group.
                try:
                    color = self._group_colors[group_num]
                except IndexError:
                    color = self._generate_random_color()
                    self._group_colors.append(color)

                # Highlight the group string. Tell the widget to highlight
                # the text using its start and end indices.
                self._highlight(group_start_idx, group_end_idx, color)

    @staticmethod
    def _generate_random_color():
        """Generate a random Qt Color from an aesthetically pleasing
        color palette.

        Logic is borrowed from http://stackoverflow.com/questions/43044/
        algorithm-to-randomly-generate-an-aesthetically-pleasing-color-palette
        """
        red = (205 + random.randint(0, 255)) / 2
        green = (205 + random.randint(0, 255)) / 2
        blue = (205 + random.randint(0, 255)) / 2
        return QColor(red, green, blue)

    def _highlight(self, start, end, color=None):
        """Highlight the text with the given color

        Arguments:
        - `start` : index in the text where the match starts
        - `end`   : index in the text where the match ends
        - `color` : the highlight color
        """
        # FIXME: Block all signals emitted by this widget. We should do this
        # temporarily to prevent going into an infinite signal-slot loop since
        # the following operations emits textChanged signal that ends up
        # calling this method (again).
        self.blockSignals(True)

        fmt = QTextCharFormat()
        # If color is None the text area is formatted with no color. This can
        # be used for clearing all the highlights in the text area
        if color:
            fmt.setBackground(color)

        cursor = QTextCursor(self.document())
        cursor.setPosition(start, QTextCursor.MoveAnchor)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        cursor.setCharFormat(fmt)

        # Unlock the signals
        self.blockSignals(False)

    def _unhighlight(self):
        """Clear all the highlighting."""
        # FIXME: A better way to clear the highlights?
        self._highlight(0, len(self.toPlainText()), color=None)
