#######################################################
# Restart all services  /+
#######################################################

echo "You are about to restart all game servers/services."
echo "Astrong, Mongo, AI, Uberdog, etc.   continue? (y/n)? "

old_stty_cfg=$(stty -g)
stty raw -echo ; answer=$(head -c 1) ; stty $old_stty_cfg # Care playing with stty
if echo "$answer" | grep -iq "^y" ;then

    #sh ../astron/unix/processes/start_mongodb.sh
    sh ../astron/unix/processes/astron.sh
    sh ../astron/unix/processes/start_pirates_services.sh
fi
