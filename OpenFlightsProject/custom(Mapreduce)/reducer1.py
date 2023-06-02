#!/usr/bin/env python3
"""reducer.py"""

import sys
lst = {}
TOP10 = 10
result = 0

# input from sys.stdin (normal_hly_sample_temperature.csv)
for line in sys.stdin:
    # remove whitespace and paser the input from mapper
    (key, val) = line.strip().split("\t")
    try:
        # convert (str to int)
        val = int(val)
    except ValueError:
        # ignore error
        continue
    # hadoop sorts map output by key before passed to reducer
    try:
        lst[key] = lst[key] + val
    except:
        lst[key] = val
# sorted top 10 countries with the most airports
for i in sorted(lst, key=lst.get, reverse=True): # highest number will first
    # write the output
    print('%s\t%s' % (i, lst[i]))
    result += 1
    if result == TOP10: # 10th then end the for loop
        break

