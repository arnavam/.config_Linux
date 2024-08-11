#!/bin/sh

# *** DEPENDS ON xprintidle AND wmctrl ***

# Screensaver to use
Screensaver=/home/arnav/.wine/TheMatrix/TheMatrixTrilogy.scr

# Minutes to wait before activating
Timeout=1

#Convert minutes to milliseconds
IDLE_TIME=$(($Timeout * 60 * 1000))

# Clobber normal Linux Screensaver and screen-blanking.
xset s off -dpms

sleep_time=$IDLE_TIME
triggered=false

# ceil() instead of floor()
while sleep $(((sleep_time + 999) / 1000)); do
	idle=$(xprintidle)
	if [ $idle -ge $IDLE_TIME ]; then
		if ! $triggered; then
			# Get a list of open windows and count the number of times YouTube &c is on it.
			youtube=$(wmctrl -l | egrep -c 'YouTube|My5|All 4')
			if [ $youtube -ge 1 ]; then
				triggered=false
				sleep_time=$IDLE_TIME
			else
				wine $Screensaver /s
				triggered=true
				sleep_time=$IDLE_TIME
			fi
		fi
	else
		triggered=false
		# Give 100 ms buffer to avoid frantic loops shortly before triggers.
		sleep_time=$((IDLE_TIME - idle + 100))
	fi
done
