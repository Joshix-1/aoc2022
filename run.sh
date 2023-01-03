#!/bin/sh

if [ ! -d "$1" ]; then
  echo "Creating dir $1 from template."
  cp -r 00 "$1"
fi

INPUT_FILE="./$1/input"

if [ "$2" = "test" ]; then
  INPUT_FILE="./$1/test-input"
elif [ -n "$2" ]; then
  echo "Invalid second argument '$2'"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "'$INPUT_FILE' doesn't exist!"
  exit 2
fi
exec env PYPY_GC_MAX=4G "./$1/main.py" < "$INPUT_FILE"
