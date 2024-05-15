#!/bin/bash
WDATE=`date +20%y%m%d`
TEXTTOINCLUDE="MAI_2024_ERASMUS"
ORIG=$1

if [ -z "$1" ];then
	echo "Need the the file to modify!"
	exit 1
fi

convert -background None -fill "rgba(64, 64, 64, 0.50)" \
    -pointsize 32 label:"$TEXTTOINCLUDE" \
    -rotate -20 \
    +repage +write mpr:TILE \
    +delete $ORIG -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite readytmp_$ORIG 

sync

convert -background None -fill "rgba(128, 34, 34, 0.35)" \
    -pointsize 16 label:"$TEXTTOINCLUDE" \
    -rotate -70 \
    +repage +write mpr:TILE \
    +delete readytmp_$ORIG -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite readytmp2_${ORIG}

convert -quality 70% readytmp2_${ORIG} ready_${ORIG}

filename=$(basename "$ready_${ORIG}")
extension="${filename##*.}"
basen="${filename%.*}"
newname="${basen}_${TEXTTOINCLUDE}.${extension}"
mv ready_${ORIG} ${newname}
ls -1 ${newname}
rm -vf readytmp*_${ORIG}
