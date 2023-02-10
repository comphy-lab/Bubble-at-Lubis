#!/bin/bash

if [ -f "log" ];
then
rm log
fi

if [ -f "dump" ];
then
rm dump
fi

if [ -f "$file" ];
then
rm $file
fi

if [ -d "intermediate" ]
then
rm -r intermediate
fi

Oho="5e-2"
Ohw="5e-3"
Oha="5e-5"
hf="0.1"
tmax="2.0"
Ldomain="4.0"
delta="0.01"
MAXlevel="12"

qcc -fopenmp -Wall -O2 $file.c -o $file -lm
export OMP_NUM_THREADS=8
./$file $Oho $Ohw $Oha $hf $tmax $Ldomain $delta $MAXlevel
