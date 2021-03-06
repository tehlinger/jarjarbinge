#!/bin/bash

SESSION=$USER

tmux -2 new-session -d -s $SESSION

tmux new-window -t $SESSION:1 -n 'Experience'
tmux send-keys "cd  /home/tehlinge/theseehlinger/trunk/jarjarbinge/master" C-m
tmux split-window -v
tmux select-pane -t 2
tmux send-keys "cd  /home/tehlinge/theseehlinger/trunk/jarjarbinge/qoe_measurers/youtube" C-m
tmux split-window -h
tmux select-pane -t 2
tmux send-keys "cd /home/tehlinge/theseehlinger/trunk/jarjarbinge/traffic_manager/" C-m
tmux set synchronize-panes on
tmux send-keys "clear" C-m
tmux set synchronize-panes off
tmux select-pane -t 0
tmux send-keys "sleep 1 ; python3 main.py qoe_requests_files/default_list.json" C-m
tmux select-pane -t 1
tmux send-keys "python3 main.py" C-m
tmux select-pane -t 2
tmux send-keys "sudo python3 main.py" C-m

#tmux -2 attach-session -t $SESSION
