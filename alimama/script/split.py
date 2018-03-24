import sys

fp_train_w = open(sys.argv[2], "w")
fp_test_w = open(sys.argv[3], "w")

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\r\n").split(" ")
  label = int(line[0])
  if label == 0 or label == 1:
    fp_train_w.write(raw_line)
  else:
    fp_test_w.write(raw_line)
