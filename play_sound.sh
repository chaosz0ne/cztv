#!/bin/bash
# play the file
cmd="exec /usr/bin/mpv $1 & echo $$! > $2.pid"
echo $cmd
sh -c "$cmd"

# if pid still exists, press button
if test -f "$2.pid"; then
    ./send_companion.py $3 $4
fi
