#!/bin/sh

# >>>> Lista_pakietow_do_odinstalowania
lista="
chromium-browser-vusolo4k
enigma2-plugin-extensions-chromium
enigma2-plugin-extensions-cutlisteditor
enigma2-plugin-extensions-dvdplayer
enigma2-plugin-extensions-dlnabrowser
enigma2-plugin-extensions-dlnaserver
enigma2-plugin-extensions-mediaplayer
enigma2-plugin-extensions-mediascanner
enigma2-plugin-extensions-minitv
enigma2-plugin-extensions-moviecut
enigma2-plugin-extensions-movieretitle
enigma2-plugin-extensions-piconmanager
enigma2-plugin-extensions-pictureplayer
enigma2-plugin-extensions-quadpip
enigma2-plugin-extensions-remotechannelstreamconverter
enigma2-plugin-extensions-tageditor
enigma2-plugin-extensions-webkithbbtv
enigma2-plugin-extensions-witaispeechtotext
enigma2-plugin-extensions-satipclient
enigma2-plugin-extensions-youtubetv
enigma2-locale-ar
enigma2-locale-ca
enigma2-locale-cs
enigma2-locale-da
enigma2-locale-el
enigma2-locale-es
enigma2-locale-et
enigma2-locale-fi
enigma2-locale-fr
enigma2-locale-fy
enigma2-locale-hr
enigma2-locale-hu
enigma2-locale-is
enigma2-locale-it
enigma2-locale-lt
enigma2-locale-lv
enigma2-locale-nl
enigma2-locale-no
enigma2-locale-pt
enigma2-locale-ru
enigma2-locale-sk
enigma2-locale-sl
enigma2-locale-sr
enigma2-locale-sv
enigma2-locale-tr
enigma2-plugin-skin-750s
enigma2-plugin-skin-atile
enigma2-plugin-skin-stylefhd
enigma2-plugin-systemplugins-3gmodemmanager
enigma2-plugin-systemplugins-autoshutdown
enigma2-plugin-systemplugins-blindscan
enigma2-plugin-systemplugins-crashreport
enigma2-plugin-systemplugins-fastchannelchange
enigma2-plugin-systemplugins-ui3dsetup
enigma2-plugin-systemplugins-uipositionsetup
enigma2-plugin-systemplugins-zappingmodeselection
"

echo "############################################" >> /tmp/enigma2_cleanUp.log
echo "reportGS.sh initiated" >> /tmp/enigma2_cleanUp.log
echo "############################################" >> /tmp/enigma2_cleanUp.log
timePeriodOnSeconds=60
DeleteLogAfterSeconds=259200

currSkin=`cat /etc/enigma2/settings|grep 'config.skin.primary_skin='|cut -d '=' -f2|cut -d '/' -f1`
SkinModsPath="/usr/share/enigma2/$currSkin/mySkin"

currEPOC=`date +%s` #returns EPOC in seconds
echo curr EPOC=$currEPOC
lastGScount=0
GScont=0
for filename in `ls /hdd/dvbapp2_crash*.log 2>/dev/null`
do
    fileEPOC=`date -r $filename +%s`
    diffEPOC=$((currEPOC - fileEPOC))
    GScont=$((GScont+1))
    if [ $diffEPOC -lt $timePeriodOnSeconds ];then
        lastGScount=$((lastGScount+1))
    fi
    if [ $diffEPOC -lt $DeleteLogAfterSeconds ];then
        cat $filename|sed -n '/^Traceback/,/^[\*]*KERNEL LOG/p' > $filename.Traceback
    fi
    rm -f $filename
done
for filename in `ls /hdd/enigma2_crash*.log 2>/dev/null`
do
    fileEPOC=`date -r $filename +%s`
    diffEPOC=$((currEPOC - fileEPOC))
    GScont=$((GScont+1))
    if [ $diffEPOC -lt $timePeriodOnSeconds ];then
        lastGScount=$((lastGScount+1))
    fi
    if [ $diffEPOC -lt $DeleteLogAfterSeconds ];then
        cat $filename|sed -n '/^Traceback/,/^[\*]*KERNEL LOG/p' > $filename.Traceback
    fi
    rm -f $filename
done

if [ $lastGScount -gt 1 ];then
    echo "Analyzed $GScont GS logs." >> /tmp/enigma2_cleanUp.log
    echo "Multiple GS's ($lastGScount) in short time detected !!!"
    echo "removing skin parts configuration"
    [ -e $SkinModsPath ] && rm -f $SkinModsPath/*.xml
    [ -e /etc/enigma2/skin_user_BlackHarmony.xml ] && rm -f /etc/enigma2/skin_user_BlackHarmony.xml
    [ -e /usr/share/enigma2/BlackHarmony/mySkin/skin_user_BlackHarmony.xml ] && rm -f /usr/share/enigma2/BlackHarmony/mySkin/skin_user_BlackHarmony.xml
    echo "Multiple GS's in short time detected, skin parts configuration has been deleted!!!" >> /tmp/enigma2_cleanUp.log
else
    echo "Analyzed $GScont GS logs. No issues found. :)"
    echo "Analyzed $GScont GS logs. No issues found. :)" >> /tmp/enigma2_cleanUp.log
fi
#################################################################### Kasowanie pakietow #########################################
echo "############################################" >> /tmp/enigma2_cleanUp.log
echo "enigma2_cleanUp.sh initiated and waiting 30s" >> /tmp/enigma2_cleanUp.log
echo "############################################" >> /tmp/enigma2_cleanUp.log
sleep 30

PacketsCount=0
UninstalledCount=0

Zainstalowane_Komponenty="`opkg list-installed`"

for pakiet in $lista;
do
 PacketsCount=$((PacketsCount+1))
 if [ "`echo $Zainstalowane_Komponenty| grep -c $pakiet`" -gt 0 ]; then
    echo "Uninstalling $pakiet..." >> /tmp/enigma2_cleanUp.log
    nice -n 10 opkg remove --force-depends $pakiet
    UninstalledCount=$((UninstalledCount+1))
 fi
done

echo "Analyzed $PacketsCount packets, uninstalled $UninstalledCount" >> /tmp/enigma2_cleanUp.log
