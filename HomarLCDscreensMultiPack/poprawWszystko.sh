#!/bin/sh
#
# NIE uruchamiać na tunerze !!!!
#

instDir='/usr/share/enigma2/HomarLCDskins'
myDir=`dirname $0`
echo $myDir

echo "zamiana skin_vfd na skin_LCD"
find $myDir -iname skin_vfd_*.xml|while read f; do
  #echo "$f"
  nf=`echo $f|sed 's/skin_vfd_/skin_LCD_/g'`
  mv -f "$f" "$nf"
done

echo "korekta nazw dla ULTIMO4K"
find $myDir -iname skin_LCD_*.xml|while read f; do
  #echo "$f"
  if [ `echo $f|grep -c 'model.ultimo4k'` -eq 1 ];then
    if [ `echo $f|grep -c 'LCD_HMR_ULTIMO4K_'` -eq 01 ];then
      nf=`echo $f|sed 's/LCD_/LCD_HMR_ULTIMO4K_/g'`
      mv -f "$f" "$nf"
    fi
  fi
done

echo "modyfikacja komponentów wewnątrz xml-i"
find $myDir -iname skin_LCD_*.xml|while read f; do
  #echo "$f"
  #używamy standardowych komponentów skórki BH
  sed -i 's/jOOzek/j00zek/g' $f 
  sed -i 's;convert type="ServiceName2";convert type="BlackHarmonyServiceName2";g' $f
  sed -i 's;vfd_skin/Homar/BingPicOfTheDay.jpg;BlackHarmony/icons/BingPicOfTheDay.jpg;g' $f #wersja aktualizowana przez BH
  # zmieniamy wszystkie ścieżki na nowe
  sed -i 's;vfd_skin/;HomarLCDskins/;g' $f
  #poprawiamy ścieżki fontów
  sed -i 's;Homar/fonts/";fonts/;g' $f
  sed -i 's;Homar/fonts/;fonts/;g' $f
  #
  #sed -i 's;;;g' $f
done
 