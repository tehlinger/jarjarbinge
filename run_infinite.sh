#!/bin/bash
exec 2<&-
while :
do
	sh launch.sh
	sleep 120
	echo "RESET"
	fish -c clean_tc
	date
done
