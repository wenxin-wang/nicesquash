#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
EXEC_DIR=$(dirname $__FILE__)
INSTANCE=$EXEC_DIR/instance

. $INSTANCE/venv/bin/activate
pip install -r $EXEC_DIR/requirements.txt
