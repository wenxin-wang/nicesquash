#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
EXEC_DIR=$(dirname $__FILE__)
INSTANCE=$EXEC_DIR/instance

sudo pacman -S --needed cronie python nvidia-settings
sudo systemctl enable cronie
sudo systemctl start cronie

. $INSTANCE/venv/bin/activate
pip install -r $EXEC_DIR/requirements.txt
