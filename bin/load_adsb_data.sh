#!/bin/bash

#flux_values=("1.31" "1.58" "1.22" "1.20" "1.16" "1.33" "1.55" "1.56" "1.32" "1.18" "1.19" "1.23")
flux_values=("1" "2" "3" "4" "5" "6" "15" "17" "28" "19" "22" "45" "47" "61" "92" "14" "26" "49" "72" "77")
size=${#flux_values[@]}
index=$(($RANDOM % $size))

sensor_values=("BKV" "BOS" "YKM" "E81" "ATW" "ANK" "EGT" "TVK" "F50" "ABY" "PTU" "D95" "SDM" "MKEA")
ssize=${#sensor_values[@]}
sindex=$(($RANDOM % $ssize))

if (( RANDOM % 2 == 0 )); then
  if (( RANDOM % 2 == 0 )); then
    /usr/bin/python3 /home/ericcobb/capstone/ADSBCommand.py --add-latency --file /home/ericcobb/capstone/data/adsb/adsb.ndjson
  else
    #/usr/bin/python3 /home/ericcobb/capstone/ADSBCommand.py --add-latency --sensor ${sensor_values[$sindex]} --flux-capacitor ${flux_values[$index]} --file /home/ericcobb/capstone/data/adsb/adsb.ndjson
    /usr/bin/python3 /home/ericcobb/capstone/ADSBCommand.py --add-latency --random-flux ${flux_values[$index]} --file /home/ericcobb/capstone/data/adsb/adsb.ndjson
  fi
else
  /usr/bin/python3 /home/ericcobb/capstone/ADSBCommand.py --add-latency --error-rate $(( ( RANDOM % 6 )  + 1 )) --file /home/ericcobb/capstone/data/adsb/adsb.ndjson
fi
if [ $? -eq 0 ]; then
  /usr/bin/python3 /home/ericcobb/capstone/bin/bulk_load_adsb.py /home/ericcobb/capstone/data/adsb/adsb.ndjson
  if [ $? -eq 0 ]; then
    echo "OK"
  else
    echo "Load Failed"
  fi
else
  echo "Sensor Poll Failed"
fi