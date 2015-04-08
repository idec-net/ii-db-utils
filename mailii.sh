#!/bin/bash

fetchmail -v
cd /path/to/letters/
/path/to/emailtoii.py
logger "mail checked"
