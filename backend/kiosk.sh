#!/bin/bash
DISPLAY=":0"
export DISPLAY=":0"
USER=uccdga

xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/"$USER"/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/"$USER"/.config/chromium/Default/Preferences

pkill chromium
/usr/bin/chromium-browser --no-sandbox --noerrdialogs --disable-infobars --kiosk "$1" &
