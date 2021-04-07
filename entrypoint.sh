#!/bin/bash

trap stop SIGTERM SIGINT SIGQUIT SIGHUP ERR

start() {
  # Start the printing loop
  python3 /app/print.py &

  # Start cupsd
  /usr/sbin/cupsd -f
}

stop() {
  exit
}

start
