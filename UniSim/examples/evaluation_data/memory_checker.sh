#!/bin/sh

while true; do
date +"%H:%M:%S"
ps -eo rss -o comm | awk '$2 == "python" || $2 == "sumo"|| $2 == "/Users/fujii/sumo/bin/sumo"' 
sleep 1s
done