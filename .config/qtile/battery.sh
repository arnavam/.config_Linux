#!/bin/bash

# Function to check battery level and display a warning
check_battery() {
	battery_level=$(cat /sys/class/power_supply/BAT0/capacity) # Change BAT0 if your battery is listed differently

	if [ "$battery_level" -le 10 ]; then
		zenity --warning --text="Battery level is ${battery_level}%. Please plug in your charger." --width=300 --height=100
		paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga # Optional sound alert
	fi
}

# Infinite loop to continuously check the battery level
while true; do
	check_battery
	sleep 60 # Check every minute
done
