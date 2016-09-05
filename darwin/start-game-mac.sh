#!/bin/sh

###
# Check if it is a symlink. If it is, then sets the correct path so python won't complain.
###
if [[ -L "${0%/*}" ]]; then
    cd `readlink "${0%/*}"  | xargs dirname | xargs dirname`
else
    cd ..
fi


if [[  whoami -eq 'easywin123' ]]; then
    export POR_PLAYCOOKIE=cj
    export POR_GAMESERVER=127.0.0.1
else

    read -p "Username: " LOGIN_COOKIE
    read -p "Gameserver: " LOGIN_SERVER

    export POR_PLAYCOOKIE=$LOGIN_COOKIE
    export POR_GAMESERVER=$LOGIN_SERVER
fi


echo "=============================="
echo "Starting Pirates Online..."
echo "Username: $LOGIN_COOKIE"
echo "Gameserver: $POR_GAMESERVER"
echo "=============================="

ppython -m pirates.piratesbase.PiratesStartDev
