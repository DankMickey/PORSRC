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
    #Since i am the only one using mac at this time
    #This is temporary, while we figure out the mac startup settings
    #Hate typing/pasting this every freaking time
    #this should be removed before this goes to production.

    export POR_PLAYCOOKIE=cj
    export POR_GAMESERVER=127.0.0.1
else

    read -p "Username: " POR_PLAYCOOKIE
    read -p "Gameserver: " POR_GAMESERVER

fi

echo "=============================="
echo "Starting Pirates Online..."
echo "Username: $POR_PLAYCOOKIE"
echo "Gameserver: $POR_GAMESERVER"
echo "=============================="

ppython -m pirates.piratesbase.PiratesStartDev
