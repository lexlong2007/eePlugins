echo "refreshing streamlink git"
cd /DuckboxDisk/github/streamlinkSOURCE
git pull

echo "copying..."

src=/DuckboxDisk/github/streamlinkSOURCE/src/streamlink
dst=/DuckboxDisk/github/eePlugins/StreamLink/usr/lib/python2.7/site-packages/streamlink

rm -f /DuckboxDisk/github/eePlugins/StreamLink/usr/lib/python2.7/site-packages/streamlink/plugins/*.py
cp -ru $src/* $dst/

if [ `cat $dst/__init__.py|grep -c '__version_date__'` -lt 1 ];then
echo "patching __init__.py ..."
  sed -i '/del get_versions/i __version_date__ = get_versions()["date"]' $dst/__init__.py
fi