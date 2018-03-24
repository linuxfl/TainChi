import sys
import time

if len(sys.argv) < 3:
  print "Usage:python preprocessing.py train_log train_ins"
  exit(1)

def timestamp_datatime(timestamp):
	format = "%Y-%m-%d %H:%M:%S"
	v = time.localtime(float(timestamp))
	dt = time.strftime(format, v)
	return dt

fp_w = open(sys.argv[2], "w")

#0:instance_id 1:item_id 2:item_category_list 3:item_property_list 4:item_brand_id 5:item_city_id 6:item_price_level 7:item_sales_level 8:item_collected_level 9:item_pv_level 10:user_id 11:user_gender_id 12:user_age_level 13:user_occupation_id 14:user_star_level 15:context_id 16:context_timestamp 17:context_page_id 18:predict_category_property 19:shop_id 20:shop_review_num_level 21:shop_review_positive_rate 22:shop_star_level 23:shop_score_service 24:shop_score_delivery 25:shop_score_description 26:is_trade

item_name = [ "instance_id", "item_id", "item_category_list", "item_property_list", "item_brand_id", "item_city_id", "item_price_level", "item_sales_level", "item_collected_level", "item_pv_level", "user_id", "user_gender_id", "user_age_level", "user_occupation_id", "user_star_level", "context_id", "context_timestamp", "context_page_id", "predict_category_property", "shop_id", "shop_review_num_level" "shop_review_positive_rate", "shop_star_level", "shop_score_service", "shop_score_delivery", "shop_score_description", "is_trade" ]

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split(" ")
  #try:
  #  if len(line[18].split(";")) < 2:
  #    print line
  #    continue
  #except:
  #  print line

  if len(line) != 27:
    #is test log
    fp_w.write("-1\001")
  else:
    #write is_trade
    fp_w.write(line[-1] + "\001")
  if len(line) != 27:
    length = len(line) + 1
  else:
    length = len(line)
  for i in range(0, length-1):
    #is item_category_list
    if i == 16:
      t = timestamp_datatime(line[i])
      fp_w.write(t[8:10] + "\001" + t[11:13] + "\001")
    else:
      if i != length-2:
        fp_w.write(line[i] + "\001")
      else:
        fp_w.write(line[i])
  fp_w.write("\n")

fp_w.close()     
