#!/bin/bash

# Start the printing loop
python3 /app/print.py &

# Start cupsd
/usr/sbin/cupsd -f
