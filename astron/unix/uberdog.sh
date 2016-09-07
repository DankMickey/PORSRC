#!/bin/sh

#kill process if it is already running
#kill -9  `pgrep -f "pirates.uberdog.ServiceStart"`
pid=$(pgrep -f "pirates.uberdog.ServiceStart")

if [[ $pid ]]; then
    kill -9  $pid
fi

#start ai server
python -m pirates.uberdog.ServiceStart > logs/uberdog.log 2>&1 &

echo "Pirates Online uberdog server - Process ID#" `pgrep -f "pirates.uberdog.ServiceStart"`
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="



