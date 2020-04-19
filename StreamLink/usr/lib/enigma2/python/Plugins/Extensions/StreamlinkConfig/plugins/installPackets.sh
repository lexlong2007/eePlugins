#/bin/sh
if [ "$1" == 'forceReinstall' ]; then
  reinstall=1
else
  reinstall=0
fi

if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
else
  PL=0
fi

opkg update > /dev/null

installed=`opkg list-installed|cut -d ' ' -f1`
paskagesList="ffmpeg
python-argparse 
python-core
python-pycrypto 
python-ctypes
python-iso3166 
python-iso639 
python-isodate 
python-futures
python-misc 
python-pkgutil
python-requests
python-shell
python-singledispatch 
python-pysocks
python-sqlite3
python-subprocess
python-websocket 
rtmpdump"

for pkg in $paskagesList;
do
  if [ `echo "$paskagesList"| grep -c $pkg` -gt 0 ];then
    if [ $reinstall -eq 0 ];then
        [ $PL -eq 1 ] && echo "$pkg jest już zainstalowany" || echo "$pkg already installed"
    else
        echo "------------------------------------------------------------"
        [ $PL -eq 1 ] && echo "$pkg jest już zainstalowany, wymuszam reinstalację" || "$pkg already installed, reinstalling it"
        echo "------------------------------------------------------------"
        opkg install --force-reinstall $pkg
    fi
  else
    opkg install $pkg
  fi
done

echo
if [ -e /var/run/streamlink.pid ];then
  [ $PL -eq 1 ] && echo "$pkg jest już zainstalowany" || echo "Restarting streamlinksrv"
  /etc/init.d/streamlinksrv restart
else
  [ $PL -eq 1 ] && echo "$pkg jest już zainstalowany" || echo "Starting streamlinksrv"
  /etc/init.d/streamlinksrv start
fi
if [ -e /var/run/streamlink.pid ];then
  [ $PL -eq 1 ] && echo "streamlinksrv uruchomiony poprawnie" || "streamlinksrv started properly"
else
  [ $PL -eq 1 ] && echo "Błąd uruchamiania streamlinksrv" || "Error starting streamlinksrv"
fi

echo
