# @j00zek 2020
#
#$1 = nazwa katalogu wtyczki
#$2 = sciezka do katalogu wtyczki
#

forkName=$1
installPath=$2
archiveURL=$3

addonName="iptvFork$forkName"

#funkcje
CleanFiles () {
rm -f /tmp/archive.tar.gz 2 > /dev/null
rm -rf /tmp/e2iplayer-master 2 > /dev/null
}
#sprawdzenie czy curl jest zainstalowany
curl --help 2>1 1>/dev/null
if [ $? -gt 0 ];then
	echo "_(ERROR: curl not installed)"
	exit 1
fi

CleanFiles
#pobieranie archiwum
echo "_(Downloading archive from) $forkName ..."
curl -s "$archiveURL" -o /tmp/archive.tar.gz
#rozpakowanie archiwum
echo "_(Unpacking archive...)"
cd /tmp/
tar -xzf /tmp/archive.tar.gz 
if [ $? -gt 0 ];then
	CleanFiles
	echo "_(ERROR: unpacking archive)"
	exit 1
fi
sync
#modyfikacja œcie¿ek i inne modyfikacje w pobranych plikach
/usr/lib/enigma2/python/Plugins/Extensions/IPTVplayersManager/scripts/patchData.sh $addonName '/tmp/e2iplayer-master/IPTVPlayer'
#kopiowanie w miejsce docelowe
if [ -e $installPath/$addonName ];then
	rm -rf $installPath/$addonName
	echo "_(Updating) $installPath/$addonName"
	successMessage="$addonName _(has been updated properly)"
	errorMessage="_(ERROR: updating) $addonName"
else
	echo "_(Installing in) $installPath/$addonName"
	successMessage="$addonName _(has been installed properly)"
	errorMessage="_(ERROR: installing) $addonName"
fi
mkdir -p $installPath/$addonName/
cp -rf /tmp/e2iplayer-master/IPTVPlayer/* $installPath/$addonName/

if [ "$installPath" != '/usr/lib/enigma2/python/Plugins/Extensions' ];then
  ln -sf $installPath/$addonName /usr/lib/enigma2/python/Plugins/Extensions/$addonName
fi
if [ $? -gt 0 ];then
	echo;echo "$errorMessage"
else
	echo;echo "$successMessage"
	echo "[doReboot]"
fi
CleanFiles
echo;echo "_(Press OK to close the window)"
exit 0

