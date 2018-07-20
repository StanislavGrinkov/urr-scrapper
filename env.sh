#! /bin/bash

# this script requires tmux base-index and pane-base-index set to 1

SESSION=pydev

tmux has-session -t "$SESSION"
if (( $? != 0 )); then
    tmux new-session -s "$SESSION" -n 'Py dev' -d
    tmux split-window -v -t "$SESSION" -p 35
    tmux send-keys -t "$SESSION:1.2" ' source venv/bin/activate && reset' C-m
    tmux send-keys -t "$SESSION:1.1" ' vim' C-m

    tmux new-window -t "$SESSION" -n 'GIT'
    tmux select-window -t "$SESSION:1"
    tmux select-pane -t "$SESSION:1.{top}"
fi
    tmux attach -t "$SESSION"

