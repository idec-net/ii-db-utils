#!/bin/bash

fetchmail -v
cd /path/to/letters/
mkdir -p echo msg

/path/to/emailtoii.py
logger "mail checked"
