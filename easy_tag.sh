#!/bin/bash
# antoine@ginies.org

# TO CHANGE ! could be a parameter...
TEXTTOINCLUDE="TAG_TO_INCLUDE"
# DO NOT CHANGE ANYTHING BELOW THIS LINE IF YOU DONT KNOW WHAT YOU ARE DOING!

# grep the current date
WDATE=`date +20%y%m%d`
# replace whitespace with underscore
TEXTTOINCLUDE=${TEXTTOINCLUDE// /_}
ORIG=$1

# Check ImageMagick is installed
if [ ! -f "/usr/bin/convert"  ];then
	echo "Please install ImageMagick"
	exit 1
fi

# Need first parameter (image to tag)
if [ -z "$1" ];then
	echo "Need the image to modify!"
	exit 1
fi

# will store the image to current path execution
directory_path=$(dirname "$ORIG")
file_name=$(basename "$ORIG")
FF="${directory_path}/${file_name}"

# Generate a random number between 0 and 11 (inclusive)
RANDOM_011=$((RANDOM % 12))
# Add 19 to the random number to get a range between 19 and 30
RANDOM_030=$((RANDOM_011 + 19))

convert -background None -fill "rgba(64, 64, 64, 0.50)" \
    -pointsize 32 label:"$TEXTTOINCLUDE" \
    -rotate -${RANDOM_030} \
    +repage +write mpr:TILE \
    +delete "$FF" -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite "readytmp_${file_name}"

# not a good idea on some system...
#sync

RANDOM_070=$((RANDOM_011 + 70))

convert -background None -fill "rgba(128, 34, 34, 0.35)" \
    -pointsize 16 label:"$TEXTTOINCLUDE" \
    -rotate -${RANDOM_070} \
    +repage +write mpr:TILE \
    +delete "readytmp_${file_name}" -alpha set \( +clone -fill mpr:TILE -draw "color 0,0 reset" \) \
    -composite "readytmp2_${file_name}"

# Reduce quality to 70%
convert -quality 70% readytmp2_${file_name} ready_${file_name}

# catch extension
filename=$(basename "$ready_${file_name}")
extension="${filename##*.}"
basen="${filename%.*}"
newname="${basen}_${TEXTTOINCLUDE}_${WDATE}.${extension}"


# rename to a correct name TEXTTOINCLUDE_WDATE
mv ready_${file_name} ${newname}
# remove tmp file
rm -f readytmp*_*
# list the file to use :)
ls -1 ${newname}
