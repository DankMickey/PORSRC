#!/bin/sh

killall pid of mongod
kill -9  `pgrep -f "pirates.ai.ServiceStart"`
kill -9  `pgrep -f "pirates.uberdog.ServiceStart"`
kill -2 `pgrep -f "astron"`
