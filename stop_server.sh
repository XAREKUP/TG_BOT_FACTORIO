#!/bin/bash
str_status=`systemctl --user status factorio_server | grep Active | cut -c 6-29`
str_eq="Active: active (running)"

if [ "$str_status" = "$str_eq" ]; then
        systemctl --user stop factorio_server >&- & echo 'Stop the server.'
else
        echo 'The server is not working.'
fi
