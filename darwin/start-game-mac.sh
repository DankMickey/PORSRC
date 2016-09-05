#!/bin/sh

###
# Check if it is a symlink. If it is, then sets the correct path so python won't complain.
###
if [[ -L "${0%/*}" ]]; then
    cd `readlink "${0%/*}"  | xargs dirname | xargs dirname`
else
    cd ..
fi

#read -p "Username: " LOGIN_COOKIE
#read -p "Gameserver: " LOGIN_SERVER

export POR_PLAYCOOKIE=cj
export POR_GAMESERVER=104.251.215.54

echo "=============================="
echo "Starting Pirates Online..."
echo "Username: $LOGIN_COOKIE"
echo "Gameserver: $LOGIN_SERVER"
echo "=============================="

ppython -m pirates.piratesbase.PiratesStartDev
