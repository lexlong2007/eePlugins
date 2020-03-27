echo "Cleaning skin files"
if [ -z $1 ];then
  searchPath=/DuckboxDisk/github/eePlugins/BH/usr/share/enigma2
else
  searchPath="$1"
fi
if [ ! -e "$searchPath" ];then
  echo "$searchPath does NOT exist, exiting"
  exit 1
fi

find "$searchPath" -type f -name "*.xml" | 
while read F 
do
#zrodla
  if [ `grep -c '"session\.BlackHarmonyMSNWeather"' < "$F"` -gt 0 ];then #zeby niepotrzebnienie ustawiac daty modyfikacji
    sed -i 's/"session\.BlackHarmonyMSNWeather"/"session.j00zekMSNWeather"/g' "$F"
  fi

  #konwertery
  if [ `grep -c 'type="ServiceName2' < "$F"` -gt 0 ];then #zeby niepotrzebnienie ustawiac daty modyfikacji
    sed -i 's/type="ServiceName2"/type="j00zekModServiceName2"/g' "$F"
  fi
  if [ `grep -c 'type="EventName' < "$F"` -gt 0 ];then #zeby niepotrzebnienie ustawiac daty modyfikacji
    sed -i 's/type="EventName"/type="j00zekModEventName"/g' "$F"
  fi
  if [ `grep -c 'type="BlackHarmonyABTCAirlyWidget"' < "$F"` -gt 0 ];then
    sed -i 's/type="BlackHarmonyABTCAirlyWidget"/type="j00zekModABTCAirlyWidget"/g' "$F"
  fi
  if [ `grep -c 'type="BlackHarmonyCaidInfo2"' < "$F"` -gt 0 ];then
    sed -i 's/type="BlackHarmonyCaidInfo2"/type="j00zekModCaidInfo2"/g' "$F"
  fi
  if [ `grep -c 'type="BlackHarmonyFrontendInfo2"' < "$F"` -gt 0 ];then
    sed -i 's/type="BlackHarmonyFrontendInfo2"/type="j00zekModFrontendInfo2"/g' "$F"
  fi
  if [ `grep -c 'type="BlackHarmonyPliExtraInfo"' < "$F"` -gt 0 ];then
    sed -i 's/type="BlackHarmonyPliExtraInfo"/type="j00zekModPliExtraInfo"/g' "$F"
  fi
#klawisze kolorow
  if [ `grep -c 'buttons/green.png' < "$F"` -gt 0 ];then
    sed -i 's;buttons/green.png;buttons/key_green.png;g' "$F"
  fi
  if [ `grep -c 'buttons/yellow.png' < "$F"` -gt 0 ];then
    sed -i 's;buttons/yellow.png;buttons/key_yellow.png;g' "$F"
  fi
  if [ `grep -c 'buttons/red.png' < "$F"` -gt 0 ];then
    sed -i 's;buttons/red.png;buttons/key_red.png;g' "$F"
  fi
  if [ `grep -c 'buttons/blue.png' < "$F"` -gt 0 ];then
    sed -i 's;buttons/blue.png;buttons/key_blue.png;g' "$F"
  fi
done
exit 0

