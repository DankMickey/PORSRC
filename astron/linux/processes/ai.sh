#!/bin/sh

#if you get an exception "No module named pymongo", install pymongo.
# python -m pip install pymongo

#kill process if it is already running
kill -9  `pgrep -f "pirates.ai.ServiceStart"`

#start ai server
python -m pirates.ai.ServiceStart > logs/ai_server.log 2>&1 &

echo "Pirates Online AI server - Process ID#" `pgrep -f "pirates.ai.ServiceStart"`
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="



