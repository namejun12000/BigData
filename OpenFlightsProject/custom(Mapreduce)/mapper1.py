#!/usr/bin/env python3
"""mapper.py"""
import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    country = line[3]
    print('%s\t%s\t' % (country, 1))