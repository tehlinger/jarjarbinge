#sudo visudo -f  /etc/sudoers.d/01_tehlinge


#Kill every single trace of the previous expriment
echo "Killing tmux server..."
tmux kill-server
echo "Done."
echo "Resetting network..."
sh /home/tehlinge/theseehlinger/trunk/jarjarbinge/reset_network.sh
echo "Done."
echo "Killing chrome..."
killall google-chrome
echo "Done."

#Relaunch
echo "Launching new chrome..."
google-chrome --new-window &
echo "Done."
echo "Launching tmux script..."
sh /home/tehlinge/theseehlinger/trunk/jarjarbinge/three_screens.tmux
echo "Done, experiment should be running."

#sudo visudo -f  /etc/sudoers.d/01_tehlinge
