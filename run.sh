#!/bin/sh
if [ ! -d $1 ]; then
    cp -r 00 $1
fi
env PYPY_GC_MAX=4G ./$1/main.py < ./$1/input
