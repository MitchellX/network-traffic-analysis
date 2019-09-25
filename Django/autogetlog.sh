#!/bin/sh

while true
do
    #get system time
    logDate=$(date "+%Y-%m-%d %H:%M:%S")
    echo [$logDate][DNS][61.135.169.125][172.20.10.2],{this is content} >> log.txt
    sleep 2
done

