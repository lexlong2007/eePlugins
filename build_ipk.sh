#!/bin/sh

myPath=$(dirname $0)
myAbsPath=$(readlink -fn "$myPath")
ipkdir=/tmp/IPK

if [ -z $1 ]; then
  echo "Error: no path to plugin provided, please us build_ipk.sh <path_to_plugin> [version]"
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
elif [ ! -e "$1/CONTROL/control" ]; then
  echo "Error: required by ipk control file missing"
  exit 0
fi
plugAbsPath=$(readlink -fn "$1")
PluginName_lower=`grep 'Package:' < $plugAbsPath/CONTROL/control|cut -d ':' -f2|xargs`
PluginPath=`grep 'DestinationPath:' < $plugAbsPath/CONTROL/control|cut -d ':' -f2|xargs`
rm -f $plugAbsPath/*.pyo 2>/dev/null
rm -f $plugAbsPath/*.pyc 2>/dev/null
if [ -z $2 ]; then
  echo "Info: no version provided, date &time of last modification will be used"
  version=`ls -atR --full-time "$plugAbsPath/"|egrep -v '^dr|version.py|control|*.mo'|grep -m 1 -o '20[12][5678].[0-9]*.[0-9]* [0-9]*\:[0-9]*'|sed 's/^20//'|sed 's/ /./'|sed 's/-/./g'|sed 's/\://g'`
  echo $version
  [ -z $version ] && echo "Error getting version" && exit 0
else
  version=$2
fi
sed -i "s/^Version\:.*/Version: $version/" $plugAbsPath//CONTROL/control
[ -e $plugAbsPath/version.py ] && echo "Version='$version'" > $plugAbsPath/version.py
find $plugAbsPath/ -type f -name *.po  -exec bash -c 'msgfmt "$1" -o "${1%.po}".mo' - '{}' \;

[ -e $ipkdir ] && sudo rm -rf $ipkdir
mkdir -p $ipkdir$PluginPath/
cp -a $plugAbsPath/* $ipkdir$PluginPath/
mv -f $ipkdir$PluginPath/CONTROL $ipkdir/
sudo chmod 755 $ipkdir/CONTROL/post*
sudo chmod 755 $ipkdir/CONTROL/pre*
sudo chown -R root $ipkdir/
cd /tmp
sudo rm -rf /tmp/IPKG_BUILD* 2>/dev/null
rm -f ~/tmp/$PluginName_lower*
$myAbsPath/tools/ipkg-build.sh $ipkdir
#echo $PluginName_lower
if [ -d ~/opkg-repository ] && [ ! -z $PluginName_lower ];then
  rm -f ~/opkg-repository/$PluginName_lower*
  mv /tmp/$PluginName_lower* ~/opkg-repository/
fi

exit 0
