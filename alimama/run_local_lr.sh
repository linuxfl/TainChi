#!/bin/bash

if [[ $1 == "test" ]];then
  python script/_1_fea.py ./data/train.log.pre ./data/train.log.fea 1
  if [[ $? -ne 0 ]];then
    exit 1
  fi
  ./bin/adfea conf/_1_run.conf
#  ./bin/gbdt_predict ./conf/gbdt.conf
  head -420717 ./instance/train.ins > ./instance/shitu.train
  tail -57421 ./instance/train.ins > ./instance/shitu.test
#  lslss=0
#  for i in `seq 1 10`;do
#    ./bin/shuffle ./instance/shitu.train ./instance/shitu.train.shuffle 500000
#    ./bin/adpa_ftrl ./instance/shitu.train.shuffle ./instance/shitu.test stream num_fea=10000208 alpha=0.1 beta=2
#    awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
#    paste -d' ' pred.txt label.txt > result.txt
#    logloss=`python ./bin/cal_metric.py result.txt | grep Logloss | awk -F' ' '{print $3}' | tail -1`
#    lslss=$(echo "$logloss + $lslss" | bc)
#  done
#  lslss=$(echo "scale=5;$lslss / 10" | bc)
#  echo $lslss
  ./bin/adpa_lbfgs ./instance/shitu.train l1_reg=0 l2_reg=50 lbfgs_stop_tol=1e-10 max_lbfgs_iter=150
  ./bin/adpa_lbfgs ./instance/shitu.test task=pred model_in=lr_model.dat
  paste -d' ' pred.txt label.txt > result.txt
  python bin/cal_metric.py result.txt
else
  cat ./data/train.log.pre > ./data/train
  cat ./data/test.log.pre >> ./data/train
  python script/_1_fea.py ./data/train ./data/train.fea 0
  ./bin/adfea conf/run_online.conf
  #./bin/gbdt_predict conf/gbdt_online.conf
  python script/split.py ./instance/ins ./instance/train.ins ./instance/test.ins
  ./bin/adpa_lbfgs ./instance/train.ins l1_reg=0 l2_reg=50 lbfgs_stop_tol=1e-10 max_lbfgs_iter=150
  ./bin/adpa_lbfgs ./instance/test.ins task=pred model_in=lr_model.dat
  echo "instance_id predicted_score" > result.txt
  awk -F' ' '{print $1}' pred.txt > pred.txt.tmp
  paste -d' ' instance_is pred.txt.tmp > tmp
  cat tmp >> result.txt
  rm tmp
fi
