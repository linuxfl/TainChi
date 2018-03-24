#!/bin/bash

head -350000 ./instance/train.ins > ./instance/shitu.train
tail -120000 ./instance/train.ins > ./instance/shitu.test

./bin/xgboost ./conf/machine_local_test.conf model_out=./model/gbdt_model.dat
./bin/xgboost ./conf/machine_local_test.conf task=pred model_in=./model/gbdt_model.dat


awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
paste -d' ' pred.txt label.txt > result.txt

python ./bin/cal_metric.py result.txt
