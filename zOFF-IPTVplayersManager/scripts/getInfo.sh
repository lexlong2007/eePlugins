# @j00zek 2020
#
#$1 = nazwa katalogu wtyczki
#$2 = sciezka do katalogu wtyczki
#

archiveURL='https://gitlab.com/mosz_nowy/infoversion/-/archive/master/infoversion-master.tar.gz'
addonName="infoversion"
addonRoot='/tmp/infoversion-master'

#funkcje
CleanFiles () {
rm -f /tmp/archive.tar.gz 2 > /dev/null
rm -rf $addonRoot 2 > /dev/null
}
#sprawdzenie czy curl jest zainstalowany
curl --help 2>1 1>/dev/null
if [ $? -gt 0 ];then
	echo "_(ERROR: curl not installed)"
	exit 1
fi

CleanFiles
#pobieranie archiwum
echo "_(Downloading archive from) $addonName git ..."
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
/usr/lib/enigma2/python/Plugins/Extensions/IPTVplayersManager/scripts/patchData.sh $addonName $addonRoot
#kopiowanie w miejsce docelowe
echo "_(Searching for iptvFork* directories) ..."
find /  -type d -name iptvFork*|while read myDir; do
  echo "_(Installing in) $myDir ..."
  cp -rf $addonRoot/* $myDir
done
CleanFiles
echo;echo "_(Press OK to close the window)"
exit 0
