#!/bin/sh

#kill process if it is already running
kill -9 `pgrep -f "astron"`

cd ..

    #
    #  Need to Update the .yml config file to use mongodb!!!!!!!!!
    #

#start ai server
if [ "$(uname)" == "Darwin" ]; then
    #Mac OS X platform
    astron/astrondmac2 --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    #GNU/Linux platform
    astron/astrondlinux --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &

elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    #Windows NT platform
    #We don't run this on Windows.....
fi

echo "Astron - Process ID#" `pgrep -f "astron"`
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="







