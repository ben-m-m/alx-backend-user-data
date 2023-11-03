#!/usr/bin/env python3
"""
filter_datum that returns the log message obfuscated:
"""
import re


def filter_datum(fields, redaction, message, separator):
    regex = re.compile(r'(?<=^|{})([^{}]+)(?={}|$)'
                       .format(re.escape(separator), re.escape(separator)))
    return regex.sub(redaction, message)
