#! /bin/bash

# this script requires tmux base-index and pane-base-index set to 1

SESSION=pydev
VENV_DIR=venv

if [[ ! -d "$VENV_DIR/" ]]; then
    python3 -m venv "$VENV_DIR"
fi

tmux has-session -t "$SESSION"
if (( $? != 0 )); then
    tmux new-session -s "$SESSION" -n 'PyDev' -d
    tmux split-window -v -t "$SESSION" -p 30
    tmux send-keys -t "$SESSION:1.2" ' ./inve.sh' C-m
    tmux send-keys -t "$SESSION:1.2" ' export PS1="( $SESSION ) $PS1"' C-m
    tmux send-keys -t "$SESSION:1.2" ' clear' C-m
    tmux send-keys -t "$SESSION:1.1" ' vim' C-m

    tmux new-window -t "$SESSION" -n 'GIT'
    tmux select-window -t "$SESSION:1"
    tmux select-pane -t "$SESSION:1.{top}"
fi

tmux attach -t "$SESSION"

