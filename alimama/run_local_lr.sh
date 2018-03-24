#!/bin/bash
./bin/adfea conf/run.conf

head -350000 ./instance/train.ins > ./instance/shitu.train
tail -120000 ./instance/train.ins > ./instance/shitu.test

if [[ $1 == "test" ]];then
	./bin/adpa_ftrl ./instance/shitu.train ./instance/shitu.test stream num_fea=5000000 alpha=0.1 beta=2

	awk -F' ' '{print $1}' ./instance/shitu.test > label.txt
	paste -d' ' pred.txt label.txt > result.txt

	python ./bin/cal_metric.py result.txt
else
	./bin/adpa_ftrl ./instance/train.ins ./instance/test.ins stream num_fea=5000000 alpha=0.1 beta=2
	echo "instance_id predicted_score" > result.txt
	paste -d' ' instance_is pred.txt > tmp
	cat tmp >> result.txt
	rm tmp
fi
