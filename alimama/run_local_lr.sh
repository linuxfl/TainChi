#!/bin/bash

if [[ $1 == "test" ]];then
  python script/fea.py ./data/train.log.pre ./data/train.log.fea
	./bin/adfea conf/run.conf
  head -350000 ./instance/train.ins > ./instance/shitu.train
  tail -120000 ./instance/train.ins > ./instance/shitu.test
  ./bin/adpa_ftrl ./instance/shitu.train ./instance/shitu.test stream num_fea=5000000 alpha=0.1 beta=2
	awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
	paste -d' ' pred.txt label.txt > result.txt
	python ./bin/cal_metric.py result.txt
else
  cat ./data/train.log.pre > ./data/train
  cat ./data/test.log.pre >> ./data/train
  python script/fea.py ./data/train ./data/train.fea
  ./bin/adfea conf/run_online.conf
  python script/split.py ./instance/ins ./instance/train.ins ./instance/test.ins
	./bin/adpa_ftrl ./instance/train.ins ./instance/test.ins stream num_fea=5000000 alpha=0.1 beta=2
	echo "instance_id predicted_score" > result.txt
	paste -d' ' instance_is pred.txt > tmp
	cat tmp >> result.txt
	rm tmp
fi
