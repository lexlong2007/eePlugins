#!/bin/sh
#This script is run just before e2

date > /tmp/enigma2_pre_start.sh.log
#mount -a
mount >>/tmp/enigma2_pre_start.sh.log

[ -e ] && rm -f /tmp/j00zekComponents.log
[ -e ] && rm -f /tmp/MSNWeatherPixmap.log
[ -e ] && rm -f /tmp/WeatherPlugin.log
[ -e ] && rm -f /tmp/AdvancedFreePlayer.log
[ -e ] && rm -f /tmp/WeatherPlugin.log

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
nice -n 10 /usr/lib/enigma2/python/Plugins/Extensions/UserSkin/scripts/reportGS.sh &
