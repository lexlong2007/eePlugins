#!/bin/bash
# to use on regular LinuxPC only
#
rootDir=`dirname $0`
cd $rootDir

for i in *.jpg
do
  if [ `identify -format '%w' $i` -ge 720 ];then
    echo converting $i
    convert $i -resize 400x225 $i.jpg
    mv $i.jpg $i
  fi
  jpegtran -copy none -progressive -optimize $i > $i.jpg #lossless optimization
  mv $i.jpg $i
done
