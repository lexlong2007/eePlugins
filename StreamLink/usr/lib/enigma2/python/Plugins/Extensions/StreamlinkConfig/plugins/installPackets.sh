#/bin/sh
updateDone=0
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
python-sqlite3
python-subprocess
python-websocket 
rtmpdump"

for pkg in $paskagesList;
do
  if [ `echo "$paskagesList"| grep -c $pkg` -gt 0 ];then
    echo "$pkg already installed"
  else
    if [[ $updateDone -eq 0 ]];then
      opkg update
      updateDone=1
    fi
    opkg install $pkg
  fi
done