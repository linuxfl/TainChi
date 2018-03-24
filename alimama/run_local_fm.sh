#!/bin/bash

head -350000 ./instance/train.ins > ./instance/shitu.train
tail -120000 ./instance/train.ins > ./instance/shitu.test

./bin/adpa_fm ./instance/shitu.train ./instance/shitu.test stream num_fea=5000000 fm_dim=3

awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
paste -d' ' pred.txt label.txt > result.txt

python ./bin/cal_metric.py result.txt
