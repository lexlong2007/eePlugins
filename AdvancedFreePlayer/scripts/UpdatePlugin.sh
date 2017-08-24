#
echo "_(Checking internet connection...)"
ping -c 1 github.com 1>/dev/null 2>&1
if [ $? -gt 0 ]; then
  echo "_(github server unavailable, update impossible!!!)"
  exit 0
fi

echo "_(Checking installation mode...)"
if `opkg list-installed 2>/dev/null|grep -q 'advancedfreeplayer'`;then
  opkg update &>/dev/null
  myPKG=`opkg list-installed 2>/dev/null | grep 'advancedfreeplayer'|cut -d ' ' -f1`
  if `opkg list-upgradable|grep -q $myPKG`;then
    opkg upgrade $myPKG
    if [ $? -gt 0 ]; then
      echo "_(AdvancedFreePlayer controlled by OPKG. Please use it for updates.)"
      exit 0
    else
      echo "_(AdvancedFreePlayer has been updated. Please restart GUI)"
      exit 0
    fi
  else
      echo "_(Latest version already installed)"
      exit 0
  fi
else
  echo "_(AdvancedFreePlayer was not installed from OPKG. Update not possible)"
  exit 0
fi

exit 0
