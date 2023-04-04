#!/bin/bash


start="1000"
end="1007"

Oho=("1e-3" "7.5e-3" "1e-2" "2.5e-2" "7.5e-2" "1e-1" "2.5e-1" "7.5e-1")

Ohw="5e-3"
Oha="5e-5"
hf="0.05"
tmax=("0.5" "0.5" "0.5" "0.5" "0.5" "0.75" "0.75" "0.75")
Ldomain="2.25"
delta="0.01"
MAXlevel="11"


for i in `seq $start $end`;
do
cd $i
qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm
export OMP_NUM_THREADS=4
./bubbleAtLubis ${Oho[$i-$start]} $Ohw $Oha $hf ${tmax[$i-$start]} $Ldomain $delta $MAXlevel
cd ..
done
