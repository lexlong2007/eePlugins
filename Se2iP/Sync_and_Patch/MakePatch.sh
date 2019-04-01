myPath=$(dirname $0)
myAbsPath=$(readlink -fn "$myPath")

cd $myAbsPath/../../Se2iP
if [ $? -gt 0 ];then
  echo "wrong path"
  exit 1
fi
mySe2iPpath=`echo $PWD`

destE2iplayerPath=$mySe2iPpath/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer

e2iplayerGTIs=/enigma2-pc/e2iplayerGITsSources

curtime=`date +"%Y%m%d_%H%M%S"`

diff -Naur $e2iplayerGTIs/SSS/e2iplayer/IPTVPlayer/ $destE2iplayerPath/ -X $mySe2iPpath/Sync_and_Patch/exclude.pats >$mySe2iPpath/Sync_and_Patch/iptvplayer-fork.patch
cp -f $mySe2iPpath/Sync_and_Patch/iptvplayer-fork.patch $mySe2iPpath/Sync_and_Patch/patches_Archive/iptvplayer-fork.$curtime.patch

