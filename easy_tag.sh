#!/bin/bash
# antoine@ginies.org

WDATE=`date +20%y%m%d`
TEXTTOINCLUDE="TAG_TO_INCLUDE"
TEXTTOINCLUDE=${TEXTTOINCLUDE// /_}
ORIG=$1

# Check ImageMagick is installed
if [ ! -f "/usr/bin/convert"  ];then
	echo "Please install ImageMagick"
	exit 1
fi

# Need first parameter (image to tag)
if [ -z "$1" ];then
	echo "Need the the file to modify!"
	exit 1
fi

# Generate a random number between 0 and 11 (inclusive)
RANDOM_011=$((RANDOM % 12))
# Add 19 to the random number to get a range between 19 and 30
RANDOM_030=$((RANDOM_011 + 19))

convert -background None -fill "rgba(64, 64, 64, 0.50)" \
    -pointsize 32 label:"$TEXTTOINCLUDE" \
    -rotate -${RANDOM_030} \
    +repage +write mpr:TILE \
    +delete $ORIG -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite readytmp_$ORIG 

# not a good idea on some system...
#sync

RANDOM_070=$((RANDOM_011 + 70))

convert -background None -fill "rgba(128, 34, 34, 0.35)" \
    -pointsize 16 label:"$TEXTTOINCLUDE" \
    -rotate -${RANDOM_070} \
    +repage +write mpr:TILE \
    +delete readytmp_$ORIG -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite readytmp2_${ORIG}

# Reduce quality to 70%
convert -quality 70% readytmp2_${ORIG} ready_${ORIG}

filename=$(basename "$ready_${ORIG}")
extension="${filename##*.}"
basen="${filename%.*}"
newname="${basen}_${TEXTTOINCLUDE}_${DATE}.${extension}"
# rename to a correct name
mv ready_${ORIG} ${newname}
# remove tmp file
rm -f readytmp*_${ORIG}
# list the file to use :)
ls -1 ${newname}
