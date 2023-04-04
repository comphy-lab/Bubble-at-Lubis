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
cp *.py $i/
cp get* $i/
cd $i

python Video.py $hf $Ldomain ${Oho[$i-$start]} $Ohw &
python TriplePoint.py $i $Ldomain $hf &
wait

ffmpeg -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p $i-TP.mp4 &
ffmpeg -framerate 60 -pattern_type glob -i 'Video/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p $i-python.mp4 &
wait

cd ..
done
