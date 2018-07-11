
startx -- -depth 30 && echo $(xwininfo -root | grep Depth) || startx -- -depth 24 && echo $(xwininfo -root | grep Depth)
