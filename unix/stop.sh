#!/bin/sh


pid[0]=$(pgrep -f "astron")
pid[1]=$(pgrep -f "pirates.ai.ServiceStart")
pid[2]=$(pgrep -f "pirates.uberdog.ServiceStart")

for i in "${pid[@]}"
do
    if [[$i ]]; then
        kill -9 $i
    fi
done