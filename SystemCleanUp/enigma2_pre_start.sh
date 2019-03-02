#!/bin/sh
#This script is run just before e2

echo "############################################" > /tmp/enigma2_cleanUp.log
echo "`date` enigma2_pre_start.sh initiated" >> /tmp/enigma2_cleanUp.log
echo "############################################" >> /tmp/enigma2_cleanUp.log
echo "Mounted devices:" >> /tmp/enigma2_cleanUp.log
#mount -a
mount >>/tmp/enigma2_cleanUp.log
echo "############################################" >> /tmp/enigma2_cleanUp.log

listaToDelete="
AdvancedFreePlayer
dynamicLCDbrightness
j00zekComponents
MSNweather
MSNWeatherPixmap
safeMode
WeatherPlugin
/usr/lib/enigma2/python/Plugins/Extensions/Tuxtxt
"

for item in $listaToDelete;
do
 [ -e $item ] && rm -f $item
 [ -e /tmp/$item.log ] && rm -f /tmp/$item.log 
done 

#	<!--map context="HelpActions">
#		<key id="KEY_HELP_OFF" mapto="displayHelp" flags="b" />
#	</map-->

#	<map context="InfobarShowHideActions">
#		<key id="KEY_HELP" mapto="toggleShow" flags="b" />
#		<key id="KEY_OK" mapto="toggleShow" flags="m" />
#		<key id="KEY_ENTER" mapto="toggleShow" flags="m" />
#		<key id="KEY_EXIT" mapto="hide" flags="m" />
#		<key id="KEY_ESC" mapto="hide" flags="m" />
#	</map>
#	<map context="InfobarPiPActions">
#		<key id="KEY_EXIT_OFF" mapto="show_hide_pip" flags="l" />
#	</map>

nice -n 10 /usr/bin/enigma2_cleanUp.sh &
