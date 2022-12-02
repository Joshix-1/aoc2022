#!/bin/sh
if [ ! -d $1 ]; then
    ./add.sh $1
fi
./$1/main.py < ./$1/input
