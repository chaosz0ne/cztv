#!/bin/bash
#let "rnd = $RANDOM"
#cp -r ffprofile profiles/$rnd
let "w = 1680 * ($1 - 1)"
echo $w
#firefox --profile profiles/$rnd --new-instance --kiosk https://ninja.c3voc.de/?view=`cat S$1_ninjasecret`\&s\&vb=5000\&buffer & sleep 2 && ./move_window.sh $w 
chromium --user-data-dir=/home/kombinat/crtmp$1 --autoplay-policy=no-user-gesture-required --new-window "%1" --window-position=$w,1080 --kiosk https://ninja.c3voc.de/?view=`cat S$1_ninjasecret`\&s\&vb=5000\&buffer & 
echo $! > s$1_pid
#echo $rnd > s$1_profile
