#!/bin/bash

mkdir binary
# Convert Python code to C
cython record.py --embed

cp *.c binary/
rm *.c
cd binary
# Make binary file from .c files
gcc $(python-config --cflags) ./record.c $(python-config --ldflags) -o record

rm *.c
