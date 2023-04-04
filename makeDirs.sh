#!/bin/bash

start="1000"
end="1007"

for i in `seq $start $end`;
do

echo $i
mkdir -p $i
scp -r *.c $i/
scp -r *get* $i/
scp -r *.py $i/
scp -r *.h $i/
scp -r *.dat $i/

done 