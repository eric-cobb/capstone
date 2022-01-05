#!/bin/bash
#
# This is just a wrapper script used as a cron job to run the 
# ADSBCommand.py script at regular intervals with various options for
# latency, error rates, and flux capacitor issues
#######################################################################

basedir="/home/ericcobb/capstone"
flux_values=("1" "2" "3" "4" "5" "6" "15" "17" "28" "19" "22" "45" "47" "61" "92" "14" "26" "49" "72" "77")
size=${#flux_values[@]}
index=$(($RANDOM % $size))

sensor_values=("BKV" "BOS" "YKM" "E81" "ATW" "ANK" "EGT" "TVK" "F50" "ABY" "PTU" "D95" "SDM" "MKEA")
ssize=${#sensor_values[@]}
sindex=$(($RANDOM % $ssize))

if (( RANDOM % 2 == 0 )); then
  if (( RANDOM % 2 == 0 )); then
    /usr/bin/python3 $basedir/ADSBCommand.py --add-latency --file $basedir/data/adsb/adsb.ndjson
  else
    /usr/bin/python3 $basedir/ADSBCommand.py --add-latency --random-flux ${flux_values[$index]} --file $basedir/data/adsb/adsb.ndjson
  fi
else
  /usr/bin/python3 $basedir/ADSBCommand.py --add-latency --error-rate $(( ( RANDOM % 6 )  + 1 )) --file $basedir/data/adsb/adsb.ndjson
fi
if [ $? -eq 0 ]; then
  /usr/bin/python3 $basedir/bin/bulk_load_adsb.py $basedir/data/adsb/adsb.ndjson
  if [ $? -eq 0 ]; then
    echo "OK"
  else
    echo "Load Failed"
  fi
else
  echo "Sensor Poll Failed"
fi