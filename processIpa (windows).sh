#!/bin/bash
trap "exit" INT

TEST_TIME=30
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
    # install app
    echo "-----installing $appId"
    echo "-----installing $appId" >> $log
    ./ideviceinstaller install $f #&> /dev/null
    if (( $? != 0 )); then
        echo "-----failure installing $appId" >> $log
    else
        # start logging network traffic
        echo "-----logging traffic $appId"
        echo "-----logging traffic $appId" >> $log
        mitmdump -p 8888 -w ./ios_log/mitm/$appId.mitm --set hardump=./ios_log/har/$appId.har --ssl-insecure &
        PID=$!
        sleep 2
        # start app and dump classes
        echo "-----starting $appId"
        echo "-----starting $appId" >> $log
        frida -U $(frida-ps -Ua | findstr $appId | awk '{print $2}') -l ./helpers/find-all-classes.js > "ios_log/classes/$appId-classes.txt" &
        PID2=$!
        sleep $TEST_TIME
    fi
    # cleanup
    echo "-----uninstalling $appId"
    echo "-----uninstalling $appId" >> $log
    ./ideviceinstaller uninstall $appId #&> /dev/null
    python helpers/home.py
    killwait $PID
    killwait $PID2
    echo "-----end testing $appId" >> $log
else
    echo "skipping $appId"
fi





