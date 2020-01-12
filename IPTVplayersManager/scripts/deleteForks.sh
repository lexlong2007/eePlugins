# @j00zek 2020
#
#$1 = nazwa katalogu wtyczki
#$2 = sciezka do katalogu wtyczki
#

#kasowanie katalogów iptvFork*
echo "_(Searching for iptvFork* directories) ..."
find /  -type d -name iptvFork*|while read myDir; do
  echo "_(Deleting) $myDir ..."
  rm -rf $myDir
done

echo;echo "_(All forks have been deleted.) _(Press OK to close the window)"
exit 0

