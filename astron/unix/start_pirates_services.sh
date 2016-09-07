cd ..



usage () {
   echo 'Usage : sh restart <service>'
    echo "                      Example: To restart all services."
    echo "                         sh restart all"
    echo "                      Example: To restart astron."
    echo "                         sh restart astron"
    echo "                      Example: To restart ai."
    echo "                         sh restart ai"
    echo "                      Example: To restart uberdog."
    echo "                         sh restart uberdog"
    echo "                      Example: To restart mongodb."
    echo "                          sh restart mongo"
    exit
}

if [[ "$service" ]]; then

    case "$service" in
        uberdog)
            sh astron/unix/uberdog.sh
            ;;
        ai)
           sh astron/unix/ai.sh
            ;;
        astron)
           sh astron/unix/astron.sh
            ;;
        mongo)
            sh ../astron/unix/mongo.sh
        ;;
        all)
           sh astron/unix/astron.sh
            sh astron/unix/ai.sh
            sh astron/unix/uberdog.sh
            ;;
        *)
            echo " Service '"$service"'  was not found, a typo herpaps?\n"
            usage
            exit 1 #
      ;;
        esac

else
    usage
fi

