@echo off
title Starting POR...

set p=%~dp0        :: sets 'p' to drive and path of batch file
cd %p%            :: changes directory

start start-mongo-server.bat
ping 127.0.0.1 -n 4 > nul
start start-astron-cluster.bat
start start-uberdog-server.bat
start start-ai-server.bat
start start-game.bat
