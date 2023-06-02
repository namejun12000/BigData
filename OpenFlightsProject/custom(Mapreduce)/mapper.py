#!/usr/bin/env python3
"""mapper.py"""
import sys


for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    airlineID = line[0]
    airlineName = line[1]
    active = line[-1]
    print('%s\t%s\t%s\t' % (airlineID,airlineName,active))