#!/bin/sh

myPath=$(dirname $0)
myAbsPath=$(readlink -fn "$myPath")
ipkdir=/tmp/IPK

if [ -z $1 ]; then
  echo "Error: no path to plugin provided, please us build)ipk.sh <path_to_plugin> [version]"
  exit 0
elif [ $(echo $1|grep -c $myPath) -eq 0 ]; then
  echo "Error: provided pluginpath is NOT subfolder of script path"
  exit 0
elif [ ! -e "$1" ]; then
  echo "Error: provided pluginpath does NOT exist"
  exit 0
elif [ ! -d "$1" ]; then
  echo "Error: provided pluginpath is NOT a directory"
  exit 0
elif [ $(echo $1|grep -c 'Plugins-') -eq 0 ]; then
  echo "Error: provided pluginpath is NOT subfolder of 'Plugins-'"
  exit 0
elif [ ! -e "$1/CONTROL/control" ]; then
  echo "Error: required by ipk control file missing"
  exit 0
fi
plugAbsPath=$(readlink -fn "$1")
PluginName=$(basename $plugAbsPath)
PluginName_lower=`grep 'Package:' < $plugAbsPath/CONTROL/control|cut -d ':' -f2| xargs`
PluginSubPath=$(basename $(dirname $plugAbsPath)|sed 's;-;/;')
PluginPath="/usr/lib/enigma2/python/$PluginSubPath/$PluginName"
if [ -z $2 ]; then
  echo "Info: no version provided, date &time of last modification will be used"
  version=`ls -atR --full-time "$plugAbsPath/" | grep -m 1 -o '20[12][5678].[0-9]*.[0-9]* [0-9]*\:[0-9]*'|sed 's/^20//'|sed 's/ /./'|sed 's/-/./g'|sed 's/\://g'`
  echo $version
  [ -z $version ] && echo "Error getting version" && exit 0
else
  version=$2
fi
[ -e $ipkdir ] && sudo rm -rf $ipkdir
mkdir -p $ipkdir$PluginPath/
cp -a $plugAbsPath/* $ipkdir$PluginPath/
mv -f $ipkdir$PluginPath/CONTROL $ipkdir/
sudo chmod 755 $ipkdir/CONTROL/post*
sed -i "s/^Version\:.*/Version: $version/" $ipkdir/CONTROL/control
sed -i "s/^Version\:.*/Version: $version/" $ipkdir/CONTROL/control
sudo chown -R root $ipkdir/
cd /tmp
sudo rm -rf /tmp/IPKG_BUILD* 2>/dev/null
rm -f ~/tmp/$PluginName_lower*
$myAbsPath/tools/ipkg-build.sh $ipkdir
echo $PluginName_lower
if [ -d ~/opkg ] && [ ! -z $PluginName_lower ];then
  rm -f ~/opkg/$PluginName_lower*
  mv /tmp/$PluginName_lower* ~/opkg/
fi

exit 0
