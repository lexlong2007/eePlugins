# @j00zek 2020
#
#$1 = nazwa katalogu wtyczki
#$2 = sciezka do katalogu wtyczki
#$3 = URL
#$4 = instalacja w katalogu oryginalnym IPTVplayer-a
if [ ! -f /usr/lib/enigma2/python/boxbranding.so ];then
  echo "_(This fork requires boxbranding.so to run, which does NOT exists in this software!!!)"
  exit 1
fi
forkName=$1
installPath=$2
archiveURL=$3
installAsFork=1; [ $4 == 'False' ] && installAsFork=0

addonName="iptvFork$forkName"

if [ "`echo $archiveURL|grep -c '.*.tar.gz$'`" -gt 0 ]; then
        archiveType="tar.gz"
elif [ "`echo $archiveURL|grep -c '.*.zip$'`" -gt 0 ]; then
        archiveType="zip"
else
        echo "_(ERROR: unknown archive type)"
        exit 1
fi
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
curl -kLs "$archiveURL" -o /tmp/archive.$archiveType
#rozpakowanie archiwum
echo "_(Unpacking archive...)"
cd /tmp/
if [ $archiveType == 'tar.gz' ];then 
        tar -xzf /tmp/archive.$archiveType
        if [ $? -gt 0 ];then
                CleanFiles
                echo "_(ERROR: unpacking archive)"
                exit 1
        fi
else #zip
        unzip --help 2>1 1>/dev/null
        if [ $? -gt 0 ];then
                CleanFiles
                echo "_(ERROR: unzip not installed)"
                exit 1
        fi
        unzip -q /tmp/archive.$archiveType
        if [ $? -gt 0 ];then
                CleanFiles
                echo "_(ERROR: unpacking archive)"
                exit 1
        fi
fi
sync
#modyfikacja sciezek i inne modyfikacje w pobranych plikach
if [ $installAsFork -eq 1 ];then
  /usr/lib/enigma2/python/Plugins/Extensions/IPTVplayersManager/scripts/patchData.sh $addonName '/tmp/e2iplayer-master/IPTVPlayer' $separateConfigs
else
  if [ -e $installPath/IPTVPlayer ];then
    if [ "$installPath" != '/usr/lib/enigma2/python/Plugins/Extensions' ];then
      rm -rf $installPath/IPTVPlayer
      rm -rf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer 2>1 1>/dev/null
    fi
  fi
fi
#kopiowanie w miejsce docelowe
if [ -e $installPath/$addonName ];then
        rm -rf $installPath/$addonName
        [ -e /usr/lib/enigma2/python/Plugins/Extensions/$addonName ] && rm -f /usr/lib/enigma2/python/Plugins/Extensions/$addonName
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
  if [ $installAsFork -eq 1 ];then
     echo "_(Linking) $addonName _(in E2 as) $addonName"
    ln -sf $installPath/$addonName /usr/lib/enigma2/python/Plugins/Extensions/$addonName
  else
     echo "_(Linking) $addonName _(in E2 as) IPTVPlayer"
     ln -sf $installPath/$addonName /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer
  fi
fi
if [ $? -gt 0 ];then
        echo;echo "$errorMessage"
else
        echo;echo "$successMessage"
        echo "[doReboot]"
fi
CleanFiles
#workarround dla braku boxbranding.so
if [ ! -f /usr/lib/enigma2/python/boxbranding.so ];then
  echo "_(Simulating missing) boxbranding.so"
  if [ `cat /proc/cpuinfo|tr '[:upper:]' '[:lower:]'|grep -c 'arm'` -gt 0 ];then cpuType='arm'
  elif [ `cat /proc/cpuinfo|tr '[:upper:]' '[:lower:]'|grep -c 'mips'` -gt 0 ];then cpuType='mips'
  elif [ `cat /proc/cpuinfo|tr '[:upper:]' '[:lower:]'|grep -c 'sh4'` -gt 0 ];then cpuType='sh4'
  else cpuType='N/A'
  fi
  echo -e "# -*- coding: utf-8 -*-
def getImageArch():
  return '$cpuType'
" > $installPath/$addonName/boxbranding.py
  cp -f $installPath/$addonName/boxbranding.py $installPath/$addonName/tools/boxbranding.py
  cp -f $installPath/$addonName/boxbranding.py $installPath/$addonName/components/boxbranding.py
fi

echo;echo "_(Press OK to close the window)"

exit 0
