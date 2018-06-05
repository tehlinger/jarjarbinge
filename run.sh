#! /bin/bash
sudo service mongod start
time=120
end=$((SECONDS+$time))
exec 2<&-
rm exp_state.txt
touch exp_state.txt
exp_done=false
IS_OVER=false
sh launch.sh
date
while [ $IS_OVER = false ]
do
    if [ \( $SECONDS -gt $end \) -o \( $exp_done = true \) ]
	then
                exp_done=true
		sleep 3
	        fish -c clean_tc
		sh launch.sh
	        date
		end=$(($end+$time))
		rm exp_state.txt
		touch exp_state.txt
		exp_done=false
		rm ~/.config/google-chrome/Default/'Extension Cookies'
		rm ~/.config/google-chrome/Default/'Network Action Predictor-journal'
		rm ~/.config/google-chrome/Default/'Network Action Predictor'
		rm ~/.config/google-chrome/Default/'Network Action Predictor'
	else
            if grep -Fxq "Done." exp_state.txt
            then
                    exp_done=true
                    echo "good"
		    rm exp_state.txt
		    touch exp_state.txt
	    else
	    	    sleep 1
            fi
    fi
done
killall chrome
fish -c clean_tc
tmux kill-server
