#!/bin/bash

#Install Flask web server
sudo apt-get install python3-flask

echo "****************************************"
echo "Flask has been installed succesfully!!"
echo "****************************************"

line="@reboot sudo python3 /home/pi/SmartLock/run.py"
(crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -