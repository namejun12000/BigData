#! /usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    record = line.split(',')
    print ('%s\t%s' % (record[3], line))