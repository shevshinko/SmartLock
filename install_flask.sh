#!/bin/bash

#Install Flask web server
sudo apt-get install python3-flask

echo "****************************************"
echo "Flask has been installed succesfully!!"
echo "****************************************"

line="@reboot sudo python3 /home/pi/SmartLock/run.py"
(sudo crontab -l; echo "$line")

read -p "Would you like to reboot now? (Y)-yes (N)-no " ASK

while [ "$ASK" != "Y"||"y" ] && [ "$ASK" != "N"||"n" ]
do
	echo "No valid answer has been given... Try Again later!"
done

if [ "$ASK" = "Y"||"y" ]; then
	#reboot
	reboot

else 
  echo "Don't forget to reboot your RPi in order to get the programme working well! Thank you in advanced!"
fi
