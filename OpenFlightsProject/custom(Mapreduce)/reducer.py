#!/usr/bin/env python3
"""reducer.py"""

import sys
YES = "Y"
NO = "N"
(airlineID, airlineName, active) = (0, None, None)

# input from sys.stdin (airlines.csv)
for line in sys.stdin:
    # remove whitespace and parse the input from mapper
    (key,val, val1) = line.strip().split("\t")
    try:
        # convert airlineID (str to int)
        key = int(key)
    except ValueError:
        # ignore error
        continue
    airlineID = key
    airlineName = val
    active = val1
    # hadoop sorts map output by key before passed to reducer
    if active == YES: # user input (Y or N); set default: "Y"
        # write the output
        print('%s\t%s\t%s' % (airlineID, airlineName, active))

