#!/bin/bash
HOME=/usr/iot
VENVDIR=$HOME/venv
cd $HOME
source $VENVDIR/bin/activate
python $HOME/run.py