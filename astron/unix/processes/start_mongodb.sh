echo "Starting  Mongodb" `pwd`
killall pid of mongod
mongod --dbpath  /data/db  --fork --syslog