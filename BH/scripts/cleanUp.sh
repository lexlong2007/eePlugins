echo "Cleaning skin files"
find /DuckboxDisk/github/eePlugins/BH/usr/share/enigma2 -name "*.xml" | 
while read F 
do
  sed -i 's/type="EventName"/type="j00zekModEventName"/g' "$F"
  sed -i 's/type="ABTCAirlyWidget"/type="BlackHarmonyABTCAirlyWidget"/g' "$F"
done
