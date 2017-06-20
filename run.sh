#!/bin/bash

SESSION_NAME='nicesquash'

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
EXEC_DIR=$(dirname $__FILE__)
LIB_DIR=$EXEC_DIR/nicesquash
MAIN=$LIB_DIR/cli.py
INSTANCE=$EXEC_DIR/instance

CWD=${CWD:-$INSTANCE}

quit() {
    echo $1
    exit $2
}

if tmux -q has-session -t ${SESSION_NAME} >/dev/null 2>&1; then
    echo "Session $SESSION_NAME already exists!"
    tmux attach-session -t ${SESSION_NAME}
    exit
fi

LOG_DIR=$CWD/logs
mkdir -p $LOG_DIR

if [ ! -e $INSTANCE/miner_algo.yml ]; then
    ln -s $LIB_DIR/miner_algo.yml $INSTANCE
fi

tmux new-session -d -s ${SESSION_NAME}
cmd="python $MAIN -d $CWD -t ${SESSION_NAME}"
if [ ! -z $BENCHMARK ]; then
    cmd="$cmd -b"
fi
tmux send-keys -t ${SESSION_NAME}:0 "$cmd" C-m

#tmux send-keys -t ${SESSION_NAME}:0.$((i+1)) "tail --follow=name $l" C-m
tmux attach-session -t ${SESSION_NAME}
