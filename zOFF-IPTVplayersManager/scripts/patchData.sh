# @j00zek 2020
#

addonName=$1
patchFolder=$2

[ -z $patchFolder ] && patchFolder='/tmp/e2iplayer-master/IPTVPlayer'
sync
#modyfikacja sciezek i inne modyfikacje
find $patchFolder -name *.py|while read pyFile; do
  echo "_(Modifying) $pyFile ..."
  sed -i "s;\"IPTVPlayer\";\"$addonName\";g" $pyFile
  sed -i "s;IPTVPlayer/;$addonName/;g" $pyFile
  sed -i "s;IPTVPlayer\.;$addonName.;g" $pyFile
  sed -i "s;config\.plugins\.iptvplayer;config.plugins.$addonName;g" $pyFile
  sed -i "s;_(\"Watch Videos Online\");'';g" $pyFile
  sed -i "s;name=((\"E2iPlayer\"));name=((\"E2iPlayer v. $addonName\"));g" $pyFile
done

if [ -d $patchFolder/Web ];then
	echo "_(Deleting Web module...)"
	rm -rf $patchFolder/Web
fi
#t³umaczenia
if [ -e $patchFolder/locale ];then
 find $patchFolder/locale -name IPTVPlayer.*|while read myFile; do
  newFile=`echo $myFile|sed "s;IPTVPlayer\.;$addonName.;g"`
  echo "_(Renaming) $myFile > $newFile"
  mv -f $myFile $newFile
 done
fi
#wylaczenie aktualizacji
if [ -e $patchFolder/iptvupdate ];then
	echo "_(Blocking original update mechanism and scripts...)"
	rm -rf $patchFolder/iptvupdate/custom/*.sh
	if [ -f $patchFolder/iptvupdate/updatemainwindow.py ];then
		sed -i "s;if 0 < len(self.list):;if 0 > len(self.list):;g" $patchFolder/iptvupdate/updatemainwindow.py
	fi
fi
sync
