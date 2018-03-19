#sudo visudo -f  /etc/sudoers.d/01_tehlinge


#Kill every single trace of the previous expriment
echo "Killing tmux server..."
tmux kill-server
echo "Done."
echo "Resetting network..."
sh ~/jarjarbinge/reset_network.sh
echo "Done."
echo "Killing chrome..."
killall chrome
echo "Done."

#Relaunch
echo "Launching new chrome..."
google-chrome --new-window &
echo "Done."
echo "Launching tmux script..."
sh ~/jarjarbinge/three_screens.tmux
echo "Done, experiment should be running."

#sudo visudo -f  /etc/sudoers.d/01_tehlinge
