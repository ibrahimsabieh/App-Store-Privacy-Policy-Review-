#!/bin/bash

trap "exit" INT

TEST_TIME=25
f=$1

echo $f

ipa=$(basename -- "$f")
appId="${ipa%.*}"

killwait ()
{
  (sleep 1; kill $1) &
  wait $1
}

#if [ ! -f ./ios_log/$appId.mitm ]; then
if [ ! -f ./ios_log/classes/$appId-classes.txt ]; then
    log=ios_log.txt
    echo "-----testing $appId"
    echo "-----testing $appId" >> $log

    #pkill mitmdump

    # install app
    echo "-----installing $appId"
    echo "-----installing $appId" >> $log
    ideviceinstaller -i $f #&> /dev/null

    if (( $? != 0 )); then
        echo "-----failure installing $appId" >> $log
    else
        # start app and dump classes
        echo "-----starting $appId"
        echo "-----starting $appId" >> $log
	sleep 5
        frida -U $(frida-ps -Ua | grep $appId | awk '{print $2}') -l ./helpers/find-all-classes.js > "ios_log/classes/$appId-classes.txt" &
        PID2=$!
        sleep $TEST_TIME
    fi

    # cleanup
    echo "-----uninstalling $appId"
    echo "-----uninstalling $appId" >> $log
    ideviceinstaller -U $appId #&> /dev/null
    python3 helpers/home.py

    killwait $PID
    killwait $PID2

    echo "-----end testing $appId" >> $log
else
    echo "skipping $appId"
fi
