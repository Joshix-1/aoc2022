#!/bin/sh
if [ ! -d $1 ]; then
    cp -r 00 $1
fi
./$1/main.py < ./$1/input
