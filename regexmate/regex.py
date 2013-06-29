#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# All Regular expression magic happens here.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 29th June 2013
#
# Licensed under MIT license. Refer COPYING for more info.


import re


class RegexValidator(object):
    """Validates the Regex syntax and find the appropriate
    matches in the input text"""

    def __init__(self, regex='', text='', flags=[]):
        self.regex = regex
        self.text = text
        self.flags = flags
        self.compiled_regex = None

    def update_regex(self, regex):
        """Update the regex pattern"""
        self.regex = regex
        self.compile_regex()

    def update_text(self, text):
        """Update the text data"""
        self.text = text

    def update_flags(self, flag, state):
        """Update the regex flags"""
        if state and flag not in self.flags:
            self.flags.append(flag)
        else:
            self.flags.remove(flag)

        self.compile_regex()

    def compile_regex(self):
        """Compile the regex"""
        if self.regex:
            flags = reduce(lambda a, b: a | b, self.flags, 0)
            try:
                self.compiled_regex = re.compile(self.regex, flags)
            except:
                # Set compiled regex to None incase of compilation errors
                self.compiled_regex = None

    def find_matches(self):
        """Return the matched items in the text data"""
        if self.text and self.compiled_regex:
            for match in self.compiled_regex.finditer(self.text):
                yield match
