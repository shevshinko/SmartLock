#!/bin/bash

#Install Flask web server
sudo apt-get install python3-flask

echo "****************************************"
echo "Flask has been installed succesfully!!"
echo "****************************************"

line="@reboot sudo python3 /home/pi/SmartLock/run.py"
(sudo crontab -l; echo "$line")

read -p "Would you like to reboot now? (Y)-yes (N)-no " ASK

while [ "$ASK" != "y" ] && [ "$ASK" != "n" ]
do
	echo "********************************"
	echo "No valid answer has been given"
	echo "********************************"
	break
done

if [ "$ASK" = "y" ]; then
	reboot

else 
  echo "Don't forget to reboot your RPi in order to get the programme working well! Thank you in advanced!"
fi
