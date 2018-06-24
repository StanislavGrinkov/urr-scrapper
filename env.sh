#! /bin/bash

# this script requires tmux setting base-index and pane-base-index set to 1

SESSION=python_dev_env

tmux new-session -s "$SESSION" -n 'Python dev venv' -d
tmux split-window -v -t "$SESSION" -p 20
tmux send-keys -t "$SESSION:1.2" ' source venv/bin/activate && reset' C-m
tmux send-keys -t "$SESSION:1.1" ' vim' C-m

tmux new-window -t "$SESSION" -n 'GIT' ' reset'
tmux select-window -t "$SESSION:1"
tmux select-pane -t "$SESSION:1.{top}"
# tmux select-pane 
tmux attach -t "$SESSION"
