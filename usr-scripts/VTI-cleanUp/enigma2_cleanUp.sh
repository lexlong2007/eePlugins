#!/bin/sh
echo "############################################" >> /tmp/enigma2_cleanUp.log
echo "enigma2_cleanUp.sh initiated and waiting 30s" >> /tmp/enigma2_cleanUp.log
echo "############################################" >> /tmp/enigma2_cleanUp.log
sleep 30
PacketsCount=0
UninstalledCount=0

Zainstalowane_Komponenty="`opkg list-installed`"

# >>>> Lista_pakietow_do_odinstalowania
lista="
chromium-browser-vusolo4k
enigma2-plugin-extensions-cutlisteditor
enigma2-plugin-extensions-dvdplayer
enigma2-plugin-extensions-chromium
enigma2-plugin-extensions-quadpip
enigma2-plugin-extensions-mediascanner
enigma2-plugin-extensions-moviecut
enigma2-plugin-extensions-movieretitle
enigma2-plugin-extensions-piconmanager
enigma2-plugin-extensions-pictureplayer
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
enigma2-plugin-systemplugins-ui3dsetup
enigma2-plugin-systemplugins-uipositionsetup
enigma2-plugin-systemplugins-zappingmodeselection
"

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
