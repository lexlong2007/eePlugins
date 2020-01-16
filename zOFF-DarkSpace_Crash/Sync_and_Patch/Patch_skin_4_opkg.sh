#!/bin/bash
myPath=$(dirname $0)
myAbsPath=$(readlink -fn "$myPath")
myAbsPath=$myAbsPath/../

cd $myAbsPath

skinPrefix="DarkSpace"

#
echo "krok 1, wywalamy wszystkie modyfikacje wtyczek i inne śmieci"
[ -d $myAbsPath/usr/lib/enigma2/python/Plugins ] && rm -rf $myAbsPath/usr/lib/enigma2/python/Plugins
[ -e $myAbsPath/usr/share/enigma2/radio.mvi ] && rm -f $myAbsPath/usr/share/enigma2/radio.mvi
[ -e $myAbsPath/usr/lib/enigma2/python/Components/WeatherMSN.py ] && rm -f $myAbsPath/usr/lib/enigma2/python/Components/WeatherMSN.py
[ -e $myAbsPath/usr/lib/enigma2/python/Components/Sources ] && rm -rf $myAbsPath/usr/lib/enigma2/python/Components/Sources
rm -rf $myAbsPath/usr/lib/enigma2/python/Components/Renderer/*MSN* 2 > /dev/null
rm -rf $myAbsPath/usr/lib/enigma2/python/Components/Converter/*MSN* 2 > /dev/null
cp -rf $myAbsPath/Sync_and_Patch/python-Components/* $myAbsPath/usr/lib/enigma2/python/Components/
cp -rf $myAbsPath/Sync_and_Patch/skin-Components/* $myAbsPath/usr/share/enigma2/DarkSpace/
#
echo "krok 2, przenosimy fonty"
[ -d $myAbsPath/usr/share/fonts ] && mv -f $myAbsPath/usr/share/fonts/* $myAbsPath/usr/share/enigma2/DarkSpace/fonts/
rm -rf $myAbsPath/usr/share/fonts
#
echo "krok 4, zmieniamy nazwy konwerterów"
cd $myAbsPath/usr/lib/enigma2/python/Components/Converter/
for orgfile in `find -type f -name '*.py'`
do
  className=`echo "$orgfile"|sed "s;.*/\(.*\)\.py;\1;"`
  if [ `echo "$orgfile"|grep -c "$skinPrefix"` -eq 0 ];then
    newFile=`echo "$orgfile"|sed "s;/;/$skinPrefix;"`
    newclassName="$skinPrefix$className"
    #echo "\t $className = $orgfile > $newFile"
    mv -f $orgfile $newFile
  else
    newFile="$orgfile"
    newclassName="$className"
    className=`echo "$newclassName"|sed "s;$skinPrefix;;"`
  fi
  #echo " -$className = $newclassName"
  sed -i "s;class $className;class $newclassName;g" $newFile #modify className in new file
  #sed -i "s;<convert type=\"$className\"[ ]*>;<convert type=\"$newclassName\">;g" $myAbsPath/usr/share/enigma2/DarkSpace/skin.xml #modify skin.xml
  #sed -i "s;<convert type=\"$className\"[ ]*/>;<convert type=\"$newclassName\" />;g" $myAbsPath/usr/share/enigma2/DarkSpace/skin.xml #modify skin.xml
  echo;echo "Zmiana $className na $newclassName w ..."
  for xmlfile in `find $myAbsPath/usr/share/enigma2/DarkSpace/ -type f -name '*.xml'`
  do
    fileName=`echo "$xmlfile"|sed "s;$myAbsPath/usr/share/enigma2/DarkSpace/;;"`
    echo " - $fileName"
    sed -i "s;<convert type=\"$className\"[ ]*>;<convert type=\"$newclassName\">;g" $xmlfile
    sed -i "s;<convert type=\"$className\"[ ]*/>;<convert type=\"$newclassName\" />;g" $xmlfile
  done
done
#
echo "krok 5, zmieniamy nazwy rendererów"
cd $myAbsPath/usr/lib/enigma2/python/Components/Renderer/
for orgfile in `find -type f -name '*.py'`
do
  className=`echo "$orgfile"|sed "s;.*/\(.*\)\.py;\1;"`
  if [ `echo "$orgfile"|grep -c "$skinPrefix"` -eq 0 ];then
    newFile=`echo "$orgfile"|sed "s;/;/$skinPrefix;"`
    newclassName="$skinPrefix$className"
    #echo "\t $className = $orgfile > $newFile"
    mv -f $orgfile $newFile
  else
    newFile="$orgfile"
    newclassName="$className"
    className=`echo "$newclassName"|sed "s;$skinPrefix;;"`
  fi
  #echo " -$className = $newclassName"
  sed -i "s;class $className;class $newclassName;g" $newFile #modify className in new file
  #sed -i "s;render=\"$className\";render=\"$newclassName\";g" $myAbsPath/usr/share/enigma2/DarkSpace/skin.xml #modify skin.xml
  echo;echo "Zmiana $className na $newclassName w ..."
  for xmlfile in `find $myAbsPath/usr/share/enigma2/DarkSpace/ -type f -name '*.xml'`
  do
    fileName=`echo "$xmlfile"|sed "s;$myAbsPath/usr/share/enigma2/DarkSpace/;;"`
    echo " - $fileName"
    sed -i "s;render=\"$className\";render=\"$newclassName\";g" $xmlfile
  done
done
exit 0
../Se2iP
if [ $? -gt 0 ];then
  echo "wrong path"
  exit 1
fi
mySe2iPpath=`echo $PWD`

destE2iplayerPath=$mySe2iPpath/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer

e2iplayerGTIs=/enigma2-pc/e2iplayerGITsSources

e2iplayerPodstawa=$e2iplayerGTIs/glowny-e2iplayer-Mario

curDate=`date +"%Y%m%d"`
if [ -e $mySe2iPpath/Sync_and_Patch/GITs_sync_time.log ];then
 . $mySe2iPpath/Sync_and_Patch/GITs_sync_time.log #get sync date
else
  syncDate=0
fi
#syncDate=0

############################## Syncing GITLAB ##############################
if [ $curDate -gt $syncDate ];then
  cd $e2iplayerGTIs/glowny-e2iplayer-Mario
  git pull
  cd $e2iplayerGTIs
  for mydir in `find -type d`
  do
    if [ -e $mydir/.git ] ; then
      echo $mydir
      cd $mydir
      git pull
      if [ $? -gt 0 ];then
        echo "Error puling fresh git data. END"
        exit 1
      fi
      cd $e2iplayerGTIs
    fi
done
  echo "syncDate=$curDate" > $mySe2iPpath/Sync_and_Patch/GITs_sync_time.log
  ############################## building differences list ##############################
  cd $e2iplayerGTIs/forks
  for mydir in `ls`
  do
    if [ -d $mydir ];then
      echo $mydir
      diff -qr $e2iplayerPodstawa/IPTVPlayer/ $e2iplayerGTIs/forks/$mydir/IPTVPlayer/ -X $mySe2iPpath/Sync_and_Patch/excludeInForksDiff.pats | cut -d ' ' -f2 >$mydir.diffList
      diff -Naur $e2iplayerPodstawa/IPTVPlayer/ $e2iplayerGTIs/forks/$mydir/IPTVPlayer/ -X $mySe2iPpath/Sync_and_Patch/excludeInForksDiff.pats >$mydir.diff_full
      diff -Naur $e2iplayerPodstawa/IPTVPlayer/ $e2iplayerGTIs/forks/$mydir/IPTVPlayer/  >$mydir.diff_complete
      [ -s $mydir.diffList ] || rm -f $mydir.diffList
      [ -s $mydir.diff_full ] || rm -f $mydir.diff_full
      [ -s $mydir.diff_complete ] || rm -f $mydir.diff_complete
      
      [ -e $mydir.diff_full ] && sed -i "s;$e2iplayerPodstawa/;;g" $mydir.diff_full
    fi
  done
fi
############################## Copying master git ##############################
rm -rf $mySe2iPpath/usr/*
mkdir -p $destE2iplayerPath
echo "Kopiuje podstawe"
cp -rf $e2iplayerPodstawa/IPTVPlayer/* $destE2iplayerPath/
############################## Copying & patching pycurl install script ##############################
#cp -rf $e2iplayerGTIs/SSS/www.iptvplayer.gitlab.io/pycurlinstall.py $mySe2iPpath/iptvplayer_rootfs/

############################## Copying additional hosts ##############################
cd $e2iplayerGTIs/hosts

for mydir in `ls`
do
  echo "Kopiuje host $mydir"
  [ -e $mydir/hosts/ ] && cp -f $mydir/hosts/* $destE2iplayerPath/hosts/
  [ -e $mydir/IPTVPlayer/hosts/ ] && cp -f $mydir/IPTVPlayer/hosts/* $destE2iplayerPath/hosts/
  [ -e $mydir/icons/ ] && cp -f $mydir/hosts/* $destE2iplayerPath/icons/
  [ -e $mydir/IPTVPlayer/icons ] && cp -f $mydir/IPTVPlayer/hosts/* $destE2iplayerPath/icons/
  [ -d $mydir/IPTVPlayer/tsiplayer ] && cp -fr $mydir/IPTVPlayer/tsiplayer $destE2iplayerPath/tsiplayer
done
############################## Copying local scripts ##############################
cp -rf $mySe2iPpath/Sync_and_Patch/files-2-copy/* $destE2iplayerPath/

############################## Applying diffs from forks ##############################
cd $destE2iplayerPath
for myFile in `ls $e2iplayerGTIs/forks/*.diff_full`
do
  if [ -f $myFile ];then
    echo "> applying $myFile"
    patch -p1 < $myFile
  fi
done
############################## Applying own patch ##############################
cd $destE2iplayerPath
echo ">>> applying own patch"
sed "s;/enigma2-pc/e2iplayerGITsSources/glowny-e2iplayer-Mario/;;g" < $mySe2iPpath/Sync_and_Patch/iptvplayer-fork.patch > /tmp/tmp.patch
patch -p1 < /tmp/tmp.patch
rm -f /tmp/tmp.patch

############################## Deleting unwanted files ##############################
rm -rf $destE2iplayerPath/icons/PlayerSelector
rm -f $destE2iplayerPath/hosts/*.txt
rm -rf $destE2iplayerPath/bin/armv5t
rm -rf $destE2iplayerPath/bin/mipsel
rm -rf $destE2iplayerPath/bin/sh4
#rm -rf $destE2iplayerPath/bin/i686

############################## Delete some unwanted hosts ##############################
cd $destE2iplayerPath
#step 1 remove all definitevely unwanted
HostsList='chomikuj favourites disabled blocked localmedia wolnelekturypl iptvplayerinfo hostwatchwrestling hostwatchwrestlinguno'
for myfile in $HostsList
do
  rm -rf ./hosts/*$myfile*
  rm -rf ./icons/*$myfile*
done

############################## modifying some hosts #############################
myFile=$destE2iplayerPath/hosts/hostinfoversion.py
sed -i 's/\(valTab\.insert.*Info o E2iPl\)/#\1/g' $myFile
sed -i 's/self.inforemote <> "0.0.0"/1==0/g' $myFile
############################## building hosts tree ##############################

for myFile in `ls /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/host*.py*`
do
  #PL
  if `grep -q 'return .*http:.*\.pl' < $myFile`;then
    file=$(basename "$myFile")
    echo "> linking $file to PL"
    ln -sf $myFile "$destE2iplayerPath/hosts/2 - Polskie/$file"
  fi
  #DE
  if `grep -q 'return .*http:.*\.de' < $myFile`;then
    file=$(basename "$myFile")
    echo "> linking $file to PL"
    ln -sf $myFile "$destE2iplayerPath/hosts/6 - Niemieckie/$file"
  fi
done

############################## Manual ##############################
HostsCategory='1 - Ulubione'
HostsList='hostyoutube hostzalukajcom'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done


HostsCategory='2 - Polskie'
HostsList='hostwptv hostmeczykipl hostzalukajcom hostkabarety'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done

HostsCategory='3 - Bajki'
HostsList='hostbajeczkiorg hostwatchcartoononline'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done

HostsCategory='4 - Sportowe'
HostsList='hostsportdeutschland hostmeczykipl hostbbcsport'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done

HostsCategory='5 - Angielskie'
HostsList='hostbbciplayer'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done

HostsCategory='6 - Niemieckie'
HostsList='hostzdfmediathek hostsportdeutschland'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done

HostsCategory='9 - Dla dorosłych'
HostsList='hostXXX'
for host in $HostsList
do
  ln -sf /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/$host.py "$destE2iplayerPath/hosts/$HostsCategory/$host.py"
done


############################## Finally, copy to enigmaPC ##############################
if [ -e /usr/local/e2/lib/enigma2/python/Plugins/Extensions/ ];then
  echo copying current version to enigma2-PC
  [ -e /usr/local/e2/lib/enigma2/python/Plugins/Extensions/IPTVPlayer ] && rm -rf /usr/local/e2/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/* || mkdir -p /usr/local/e2/lib/enigma2/python/Plugins/Extensions/IPTVPlayer
  cp -rf $destE2iplayerPath/* /usr/local/e2/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/
fi

exit 0 
publicGitRoot=$GITroot/crossplatform_iptvplayer
daemonDir=$publicGitRoot/IPTVdaemon
KaddonDir=$publicGitRoot/addon4KODI/neutrinoIPTV
NpluginDir=$publicGitRoot/addon4neutrino/neutrinoIPTV
publicGitDir=$publicGitRoot/IPTVplayer

############################################################
############################## logos structure & names ##############################
rm -f $publicGitDir/icons/*
mv -f $publicGitDir/icons/logos/*.png $publicGitDir/icons/
cp -a ~/Archive/iptvplayerXXX-GitLab-master-version/IPTVPlayer/icons/logos/XXXlogo.png $publicGitDir/icons/XXX.png
cp -a ~/Archive/iptvplayer-infoversion-host/icons/logos/infologo.png $publicGitDir/icons/infoversion.png
rm -rf $publicGitDir/icons/logos/
rm -rf $publicGitDir/icons/favourites*
cd $publicGitDir/icons/
for myfile in `ls ./*logo.png`
do
  newName=`echo $myfile|sed 's/logo//'`
  mv -f $myfile $newName
done
############################## hosts names ##############################
cd $publicGitDir/hosts/
rm -f ./list.txt
for myfile in `ls ./*.py`
do
  newName=`echo $myfile|sed 's/host//'`
  [ $myfile == $newName ] || mv -f $myfile $newName
done
############################## Adapt congig.py file ##############################
myFile=$publicGitDir/icomponents/iptvconfigmenu.py
sed -i 's/import ConfigBaseWidget,/import/' $myFile
sed -i '/class ConfigMenu(ConfigBaseWidget)/,$d' $myFile
#remove unnecesary stuff
sed -i 's;from iptvpin import IPTVPinWidget;;g
  
  ' $myFile
############################## cleaning unused components #######################################################################################
echo 'Cleaning not used components from scripts...'
cd $publicGitDir
for myfile in `find -type f -name '*.py'`
do
  #echo $myfile
  
  sed -i "s;\(from .*\.\)components\(\.iptvplayerinit\);\1dToolsSet\2;g" $myfile #use own fake initscript
  sed -i "s;\(from .*\.\)tools\(\.iptvtools\);\1dToolsSet\2;g" $myfile #use own fake tools script
  sed -i "s;\(from .*\.\)components\.recaptcha_v2widget;\1dToolsSet.recaptcha_v2widget;g" $myfile #use own fake capcha
  toDel='MessageBox';[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='ConfigBaseWidget';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='ConfigHostsMenu';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='IPTVDirectorySelectorWidget';	[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='IPTVSetupMainWidget';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='Screen';			[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='VirtualKeyBoard';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='Label';			[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='ConfigListScreen';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='boundFunction';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='IPTVUpdateWindow';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='ActionMap';			[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='ConfigExtMoviePlayer';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  toDel='IPTVMultipleInputBox';		[[ `grep -c $toDel<$myfile` -gt 1 ]] || sed -i "/import .*$toDel/d" $myfile
  #toDel='self.console_appClosed_conn';	[[ `grep -q $toDel<$myfile` ]] || sed -i "/$toDel/d" $myfile
  #toDel='self.console_stderrAvail_conn';[[ `grep -q $toDel<$myfile` ]] || sed -i "/$toDel/d" $myfile
  
  #adding missing
  toAdd='iptvplayerinit import TranslateTXT as _';         [[ `grep -c "$toAdd"<$myfile` -ge 1 ]] || sed -i "/ihost import IHost/a from Plugins.Extensions.IPTVPlayer.dToolsSet.iptvplayerinit import TranslateTXT as _" $myfile
  
  #probably to del later ;)
  #toDel='eConsoleAppContainer';		[[ `grep -c $toDel<$myfile` -ge 1 ]] && echo $myfile #sed -i "s/\(^.*$toDel\)/#\1/g" $myfile
  sed -i 's/\(raise BaseException\)("\(.*\)")/printDBG("\1(\2)")/g' $myfile
  #sed -i "s/\(getListForItem begin\)\(['\"]+\)/\1 Index=%d, selItem=%s \2 % (Index,str(selItem))/g" $myfile

  # NEW folders structure
  sed -i "s;\(from .*\.\)components\(.*\);\1icomponents\2;g" $myfile #new folders structure to workarround with fat issues
  sed -i "s;\(from .*\.\)tools\(.*\);\1itools\2;g" $myfile #new folders structure to workarround with fat issues
  sed -i "s;\(import .*\.\)components\(.*\);\1icomponents\2;g" $myfile #new folders structure to workarround with fat issues
  sed -i "s;\(import .*\.\)tools\(.*\);\1itools\2;g" $myfile #new folders structure to workarround with fat issues
  sed -i "s;\(import .*\dToolsSet.\)itools\(.*\);\1iptvtools\2;g" $myfile #new folders structure to workarround with fat issues
  sed -i "s;getDesktop(0).size().width();1980;g" $myfile #e2 emulator does not have it, so setting 1980 FHD it eill br nrvrt used
done
#removing local imports from the list
echo 'Removing some hosts and adding couple new 3rd party...'
cd $publicGitDir

#specific for hosts
sed -i "s/\(_url.*hostXXX.py\)/\1DISABLED/g" $publicGitDir/hosts/XXX.py
############################## Syncing contrib apps ##############################
#echo 'Syncing contrib apps...'
#wget -q http://iptvplayer.pl/resources/bin/sh4/exteplayer3_ffmpeg3.0 -O $publicGitDir/bin/sh4/exteplayer3
#wget -q http://iptvplayer.pl/resources/bin/sh4/uchardet -O $publicGitDir/bin/sh4/uchardet


############################## Delete hosts with captcha ##############################
cd $publicGitDir/hosts
for myfile in `find -type f -name '*.py'`
do
  toDel='captcha';
  if [[ `grep -c $toDel<$myfile` -ge 1 ]];then 
    rm -rf $publicGitDir/hosts/*$myfile*
    rm -rf $publicGitDir//icons/*$myfile*
    echo "deleting captcha host: $myfile"
  fi
done

###change some default values
sed -i "s;\(config\.plugins\.iptvplayer\.\iplaUseDF.*ConfigYesNo.default[ ]*=[ ]*\)True;\1False;" $publicGitDir/hosts/ipla.py
############################## copying to GIT public repo to fit license ##############################
#echo 'Syncing public GIT...'
#cp -a $publicGitDir/* $GITroot/cmdline_iptvplayer/
#rm -rf $GITroot/cmdline_iptvplayer/dToolsSet
#rm -f $GITroot/cmdline_iptvplayer/IPTVdaemon.py
#rm -f $GITroot/cmdline_iptvplayer/testcmdline.py
#rm -f $GITroot/cmdline_iptvplayer/cmdlineIPTV.py

###################### step 2 create lua list with titles
cd $publicGitDir
echo "HostsList={ ">$NpluginDir/luaScripts/hostslist.lua
echo "# -*- coding: utf-8 -*-
HostsList=[ ">$daemonDir/dToolsSet/hostslist.py
for myfile in `cd ./hosts;ls ./*.py|grep -v '_init_'|sort -fi`
do
    fileNameRoot=`echo $myfile|sed 's/\.\/\(.*\)\.py/\1/'`
    tytul=`sed -n '/def gettytul..:/ {n;p}' ./hosts/$myfile`
    if `grep -v '[ \t]*#'< ./hosts/$myfile|grep -q 'optionList\.append(getConfigListEntry('`;then
	hasConfig=1
    else
	hasConfig=0
    fi
    if ! `echo $tytul|grep -q 'return'`;then
      tytul=$fileNameRoot
    else
      #tytul=`echo $tytul|cut -d "'" -f2|sed "s;http://;;"|sed "s;/$;;"|sed "s;www\.;;"`
      tytul=`echo $tytul|sed "s/^.*['\"]\(.*\)['\"].*$/\1/"|sed 's/^ *//;s/ *$//;s/http[s]*://;s/\///g;s/www\.//'`
    fi
    #echo "	{id=\"$fileNameRoot\", title=\"$tytul\", fileName=\"hosts/$fileNameRoot.py\", logoName=\"icons/$fileNameRoot.png\", type=\"py\"},">>$NpluginDir/luaScripts/hostslist.lua
    echo "      {id=\"$fileNameRoot\", title=\"$tytul\", type=\"py\"},">>$NpluginDir/luaScripts/hostslist.lua
    echo "	(\"$fileNameRoot\", \"$tytul\"),">>$daemonDir/dToolsSet/hostslist.py
done
echo "	]">>$daemonDir/dToolsSet/hostslist.py
##################### step 3 the same for lua scripts
cd $NpluginDir
for myfile in `cd ./luaHosts;ls ./*.lua|sort -fi`
do
    fileNameRoot=`echo $myfile|sed 's/\.\/\(.*\)\.lua/\1/'`
    tytul=`sed -n '/def gettytul..:/ {n;p}' ./luaHosts/$myfile`
    if ! `echo $tytul|grep -q 'return'`;then
      tytul=$fileNameRoot
    else
      tytul=`echo $tytul|cut -d "'" -f2|sed "s;http://;;"|sed "s;/$;;"|sed "s;www\.;;"`
    fi
    echo "	{id=\"$fileNameRoot\", title=\"$tytul\", fileName=\"luaHosts/$fileNameRoot.lua\", logoName=\"luaHosts/$fileNameRoot.png\", type=\"lua\"},">>$NpluginDir/luaScripts/hostslist.lua
done
echo "	}">>$NpluginDir/luaScripts/hostslist.lua
###################### step 4 create list of possible configs
cd $publicGitDir
echo "#Aby ustawic jakas opcje nalezy skopiowac jej nazwe do pliku E2settings.conf i wpisac jej wartosc" > $NpluginDir/../IPTV-E2settings.list
echo "#Przyklad:" >> $NpluginDir/../IPTV-E2settings.list
echo "" >> $NpluginDir/../IPTV-E2settings.list
echo "#Lista mozliwych opcji konfiguracyjnych IPTVplayer-a:" >> $NpluginDir/../IPTV-E2settings.list
for myfile in `find -type f -name '*.py'`
do
  #echo $myfile
  cat $myfile| egrep -v 'extplayer|gstplayer|MIPS|ARM|software_decode' | grep -o "config\.plugins\.iptvplayer\..*=[ ]*Config.*$" >> $NpluginDir/../IPTV-E2settings.list
done
