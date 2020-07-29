#!/usr/bin/env bash
while true; do
    cnt=`ps -ef |grep -v grep| grep "ffmpeg" | wc -l`
    if [ $cnt -lt 1 ]
    then
        echo "Killed all ffmpeg!"
        break
    fi
    # else
    echo "$cnt left to kill..."
    ps -ef |grep -v grep| grep "ffmpeg" | head -10 | awk -F ' ' '{print $2}' | xargs kill
    echo "kill 10 ffmpeg per 3 seconds"
    sleep 3
done