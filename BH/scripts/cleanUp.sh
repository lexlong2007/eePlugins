echo "Cleaning skin files"
find /DuckboxDisk/github/eePlugins/BH/usr/share/enigma2 -name "*.xml" | 
while read F 
do
  if [ `grep -c 'type="ServiceName2' < "$F"` -gt 0 ];then #zeby niepotrzebnienie ustawiac daty modyfikacji
    sed -i 's/type="ServiceName2"/type="j00zekModServiceName2"/g' "$F"
  fi
  if [ `grep -c 'type="EventName' < "$F"` -gt 0 ];then #zeby niepotrzebnienie ustawiac daty modyfikacji
    sed -i 's/type="EventName"/type="j00zekModEventName"/g' "$F"
  fi
  if [ `grep -c 'type="ABTCAirlyWidget"' < "$F"` -gt 0 ];then
    sed -i 's/type="ABTCAirlyWidget"/type="BlackHarmonyABTCAirlyWidget"/g' "$F"
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
done
exit 0
