#!/bin/bash

if [[ $1 == "test" ]];then
#  python script/_1_fea.py ./data/train.log.pre ./data/train.log.fea 1
  if [[ $? -ne 0 ]];then
    exit 1
  fi
  ./bin/adfea conf/_1_run.conf
  head -420717 ./instance/train.ins > ./instance/shitu.train
  tail -57421 ./instance/train.ins > ./instance/shitu.test

  ./bin/xgboost ./conf/machine_local_test.conf model_out=./model/gbdt_model.dat
  ./bin/xgboost ./conf/machine_local_test.conf task=pred model_in=./model/gbdt_model.dat
  ./bin/xgboost ./conf/machine_local_test.conf task=dump model_in=./model/gbdt_model.dat name_dump=./model/gbdt_model.json

  awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
  paste -d' ' pred.txt label.txt > result.txt
  python ./bin/cal_metric.py result.txt
else
  cat ./data/train.log.pre > ./data/train
  cat ./data/test.log.pre >> ./data/train
  python script/_1_fea.py ./data/train ./data/train.fea 0
  ./bin/adfea conf/run_online.conf
  python script/split.py ./instance/ins ./instance/train.ins ./instance/test.ins
  tail -10000 ./instance/ins > ./instance/valid.ins

  ./bin/xgboost ./conf/machine.conf model_out=./model/gbdt_model.dat
  ./bin/xgboost ./conf/machine.conf task=pred model_in=./model/gbdt_model.dat
  ./bin/xgboost ./conf/machine.conf task=dump model_in=./model/gbdt_model.dat name_dump=./model/gbdt_model.json
  echo "instance_id predicted_score" > result.txt
  paste -d' ' instance_is pred.txt > tmp
  cat tmp >> result.txt
  rm tmp
fi
