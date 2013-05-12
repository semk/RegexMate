#! /usr/bin/env python
# -*- coding: utf-8 -*-


import re


class RegexValidator(object):
    """Validates the Regex syntax and find the appropriate
    matches in the input text"""
    
    def __init__(self, regex, text):
        self.regex = regex
        self.text = text

    def validate_regex(self):
        pass
        
    def find_matches(self):
        pass