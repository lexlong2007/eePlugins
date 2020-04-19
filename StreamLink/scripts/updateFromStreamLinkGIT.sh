echo "refreshing streamlink git"
cd /DuckboxDisk/github/streamlinkSOURCE
git pull

echo "copying..."

src=/DuckboxDisk/github/streamlinkSOURCE/src
dst=/DuckboxDisk/github/eePlugins/StreamLink/usr/lib/python2.7/site-packages

rm -f /DuckboxDisk/github/eePlugins/StreamLink/usr/lib/python2.7/site-packages/streamlink/plugins/*.py
cp -ru $src/streamlink/* $dst/streamlink/
cp -ru $src/streamlink_cli/* $dst/streamlink_cli/
cp -f $dst/../../../../scripts/unofficialPlugins/* $dst/streamlink/plugins/

if [ `cat $dst/streamlink/__init__.py|grep -c '__version_date__'` -lt 1 ];then
  echo "patching __init__.py ..."
  sed -i '/del get_versions/i __version_date__ = get_versions()["date"]' $dst/streamlink/__init__.py
fi

if [ `cat $dst/streamlink/utils/l10n.py|grep -c 'except ImportError as e:'` -lt 1 ];then
  echo "patching l10n.py ..."
  sed -i 's/\(^except ImportError\)\(:.*\)/\1 as e\2\n    print str(e)\n/' $dst/streamlink/utils/l10n.py
fi
