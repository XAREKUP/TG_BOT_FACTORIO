#!/bin/bash
server_version=`cat /opt/factorio/data/base/info.json | grep -oP '[0-9]*\.[0-9]*\.[0-9]*'`
actual_version=`curl -s https://factorio.com/get-download/stable/headless/linux64 | grep -oP '[0-9]*\.[0-9]*\.[0-9]*' | tail -n 1`
#echo $server_version
#echo $actual_version
if [ "$server_version" = "$actual_version" ]; then
        echo "The server has the latest available stable version: ${server_version}"
else
        echo "Warning: There is a new stable version: ${actual_version}. Current server version: ${server_version}"
fi
