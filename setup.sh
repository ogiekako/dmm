#!/bin/bash

tmp=$(mktemp)
crontab -u $USER -l > $tmp

echo "5 0 * * * PATH=$PATH:\$PATH $(pwd)/reserve.py --headless 2> /tmp/dmm.log" >> $tmp

crontab -u $USER $tmp
