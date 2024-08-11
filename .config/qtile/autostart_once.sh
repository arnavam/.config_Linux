#!/bin/sh

# Start picom
picom &
#/usr/bin/xscreensaver & disown
/home/arnav/.wine/winss.sh & #for matrix screensaver

./battery.sh & #to check battery
xmodmap -e 'keycode 80='
