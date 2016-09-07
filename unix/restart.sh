#######################################################
# Restart all services  /+
#######################################################

export service="${1%/*}"

sh ../astron/unix/start_pirates_services.sh
