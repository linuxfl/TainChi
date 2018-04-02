#!/bin/bash

if [[ $1 == "test" ]];then
  python script/_1_fea.py ./data/train.log.pre ./data/train.log.fea 1
  if [[ $? -ne 0 ]];then
    exit 1
  fi
  ./bin/adfea conf/_1_run.conf
  ./bin/gbdt_predict ./conf/gbdt.conf
  head -420717 ./instance/train.ins.gbdt > ./instance/shitu.train
  tail -57421 ./instance/train.ins.gbdt > ./instance/shitu.test
  lslss=0
  for i in `seq 1 10`;do
    ./bin/shuffle ./instance/shitu.train ./instance/shitu.train.shuffle 500000
    ./bin/adpa_fm ./instance/shitu.train.shuffle ./instance/shitu.test stream num_fea=10000208 fm_dim=3 alpha=0.07 beta=3 alpha_fm=0.01 beta_fm=3 l2_fm_reg=0. l2_reg=0.1
    awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
    paste -d' ' pred.txt label.txt > result.txt
    logloss=`python ./bin/cal_metric.py result.txt | grep Logloss | awk -F' ' '{print $3}' | tail -1`
    lslss=$(echo "$logloss + $lslss" | bc)
  done
  lslss=$(echo "scale=5;$lslss / 10" | bc)
  echo $lslss
else
  cat ./data/train.log.pre > ./data/train
  cat ./data/test.log.pre >> ./data/train
  python script/_1_fea.py ./data/train ./data/train.fea 0
  ./bin/adfea conf/run_online.conf
  ./bin/gbdt_predict conf/gbdt_online.conf
  python script/split.py ./instance/ins.gbdt ./instance/train.ins ./instance/test.ins
  ./bin/shuffle ./instance/train.ins ./instance/train.ins.shuffle 500000
  ./bin/adpa_fm ./instance/train.ins.shuffle ./instance/test.ins stream num_fea=10000208 fm_dim=3 alpha=0.07 beta=3 alpha_fm=0.01 beta_fm=3 l2_fm_reg=0. l2_reg=0.1
  echo "instance_id predicted_score" > result.txt
  paste -d' ' instance_is pred.txt > tmp
  cat tmp >> result.txt
  rm tmp
fi
