#!/bin/bash
server_version=`cat /opt/factorio/data/base/info.json | grep -oP '[0-9]*\.[0-9]*\.[0-9]*'`
actual_version=`curl -s https://factorio.com/download/sha256sums/ | grep factorio_linux | head -n 1 | grep factorio_linux | grep -oP '[0-9]*\.[0-9]*\.[0-9]*'`
#echo $server_version
#echo $actual_version
if [ "$server_version" = "$actual_version" ]; then
        echo "The server has the latest available version: ${server_version}"
else
        echo "Warning: There is a new version: ${actual_version}. Current server version: ${server_version}"
fi
