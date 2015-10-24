#!/bin/bash
# Downsize Raspberry Pi image to 110% of its minimum size
# http://sirlagz.net/2013/03/10/script-automatic-rpi-image-downsizer/

strImgFile=$1
strHelp="Usage: bash ./$0 rpi.img"

if [[ $EUID -ne 0 ]]; then
# not run as root
echo ""
echo "**********************************"
echo "*** This script should be run as root ***"
echo "**********************************"
echo ""
exit
fi

if [[ -z $1 ]]; then
echo $strHelp
exit
fi

if [[ ! -e $1 || ! $(file $1) =~ "x86" ]]; then
echo "Error: Not an image file, or file doesn't exist"
exit
fi

partinfo=`parted -m $1 unit B print`
partnumber=`echo "$partinfo" | grep ext4 | awk -F: ' { print $1 } '`
partstart=`echo "$partinfo" | grep ext4 | awk -F: ' { print substr($2,0,length($2)-1) } '`
loopback=`losetup -f --show -o $partstart $1`
e2fsck -f $loopback
minsize=`resize2fs -P $loopback | awk -F': ' ' { print $2 } '`

# Modified minsize calc by Kevin Rattai
# Original minsize produces 0bytes on partition, calculated as:
# minsize=`echo “$minsize+1000” | bc`
minsize=`echo "($minsize+($minsize*0.1))/1" | bc`

resize2fs -p $loopback $minsize
sleep 1
losetup -d $loopback
partnewsize=`echo "$minsize * 4096" | bc`
newpartend=`echo "$partstart + $partnewsize" | bc`
part1=`parted $1 rm 2`
part2=`parted $1 unit B mkpart primary $partstart $newpartend`
endresult=`parted -m $1 unit B print free | tail -1 | awk -F: ' { print substr($2,0,length($2)-1) } '`
truncate -s $endresult $1

