#!/usr/bin/env bash
while true; do
    cnt=`ps -ef |grep -v grep| grep "ffplay" | wc -l`
    if [ $cnt -lt 1 ]
    then
        echo "Killed all ffplay!"
        break
    fi
    # else
    echo "$cnt left to kill..."
    ps -ef |grep -v grep| grep "ffplay" | head -10 | awk -F ' ' '{print $2}' | xargs kill
    echo "kill 10 ffplay per 1 seconds"
    sleep 1
done