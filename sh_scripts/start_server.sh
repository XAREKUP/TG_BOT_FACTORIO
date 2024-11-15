#!/bin/bash
str_status=`systemctl --user status factorio_server | grep Active | cut -c 6-29`
str_eq="Active: active (running)"

if [ "$str_status" = "$str_eq" ]; then
	echo 'The server is already running.'
else
	systemctl --user start factorio_server >&- & echo 'Start the server.'
fi
