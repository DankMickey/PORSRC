#!/bin/sh

#kill process if it is already running
kill -9 `pgrep -f "astron"`

cd ..

#start ai server
astron/astrondmac2 --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &

echo "Astron - Process ID#" `pgrep -f "astron"`
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="







