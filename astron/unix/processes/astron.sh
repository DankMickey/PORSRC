#!/bin/sh

echo "$(uname)"

#kill process if it is already running
kill -9 `pgrep -f "astron"`

cd ..

    #
    #  Need to Update the .yml config file to use mongodb!!!!!!!!!
    #

#start ai server
if [[ "$(uname)" == "Darwin" ]]; then
    #Mac OS X platform
    astron/astrondmac2 --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &

elif [[  $(uname) =~ ^Linux$ ]]; then
    #GNU/Linux platform
    astron/astrondlinux --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &
fi

echo "Astron - Process ID#" `pgrep -f "astron"`
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="







