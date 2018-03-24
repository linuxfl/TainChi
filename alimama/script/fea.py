import sys
import time

if len(sys.argv) < 3:
  print "Usage:python preprocessing.py train_log train_ins"
  exit(1)

fp_w = open(sys.argv[2], "w")

#0:label 1:instance_id 2:item_id 3:item_category_list 4:item_property_list 5:item_brand_id 6:item_city_id 7:item_price_level 8:item_sales_level 9:item_collected_level 10:item_pv_level 11:user_id 12:user_gender_id 13:user_age_level 14:user_occupation_id 15:user_star_level 16:context_id 17:day 18:hour 19:context_page_id 20:predict_category_property 21:shop_id 22:shop_review_num_level 23:shop_review_positive_rate 24:shop_star_level 25:shop_score_service 26:shop_score_delivery 27:shop_score_description

#item and user and shop show conversion
item_dict = {}
user_dict = {}
shop_dict = {}

shop_on_review_num_level = {}
review_num_level_dict = {}
shop_on_review_position_rate = {}
review_position_rate_dict = {}
shop_on_star_level = {}
shop_on_score_service = {}
shop_on_score_delivery = {}
shop_on_score_descrip = {}

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split("\001")
  if int(line[0]) == -1:
    continue
  shop_id = line[21]  
  item_id = line[2]
  user_id = line[11]
  shop_id = line[21]
  review_num_level = line[22]
  review_position_rate = line[23]
  label = line[0]
  if review_num_level not in shop_on_review_num_level:
     shop_on_review_num_level[review_num_level] = {}
  if shop_id not in shop_on_review_num_level[review_num_level]:
     shop_on_review_num_level[review_num_level][shop_id] = {"show":0, "conv":0}
  shop_on_review_num_level[review_num_level][shop_id]["show"] += 1
  shop_on_review_num_level[review_num_level][shop_id]["conv"] += int(label)
  if review_num_level not in review_num_level_dict:
     review_num_level_dict[review_num_level] = {"show":0, "conv":0}
  review_num_level_dict[review_num_level]["show"] += 1
  review_num_level_dict[review_num_level]["conv"] += int(label)
  if review_position_rate not in shop_on_review_position_rate:
    shop_on_review_position_rate[review_position_rate] = {}
  if shop_id not in shop_on_review_position_rate[review_position_rate]:
    shop_on_review_position_rate[review_position_rate][shop_id] = {"show":0, "conv":0}
  shop_on_review_position_rate[review_position_rate][shop_id]["show"] += 1
  shop_on_review_position_rate[review_position_rate][shop_id]["conv"] += int(label)
  if review_position_rate not in review_position_rate_dict:
    review_position_rate_dict[review_position_rate] = {"show":0, "conv":0}
  review_position_rate_dict[review_position_rate]["show"] += 1
  review_position_rate_dict[review_position_rate]["conv"] += int(label)

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split("\001")
  label = line[0]

  item_id = line[2]
  user_id = line[11]
  shop_id = line[21]
  review_num_level = line[22]
  review_position_rate = line[23]

  fp_w.write(raw_line.strip("\r\n") + "\001")
  if item_id in item_dict:
    fp_w.write("%s\001%s\001"%(item_dict[item_id]["show"], item_dict[item_id]["conv"]))
  else:
    fp_w.write("0\0010\001")
  if shop_id in shop_dict:
    fp_w.write("%s\001%s\001"%(shop_dict[shop_id]["show"], shop_dict[shop_id]["conv"]))
  else:
    fp_w.write("0\0010\001")
  if user_id in user_dict:
    fp_w.write("%s\001%s\001"%(user_dict[user_id]["show"], user_dict[user_id]["conv"]))
  else:
    fp_w.write("0\0010\001")
  #write other fea
  if review_num_level not in shop_on_review_num_level:
    fp_w.write("0\0010\001")
  else:
    if shop_id not in shop_on_review_num_level[review_num_level]:
      fp_w.write("0\0010\001")
    else:
      fp_w.write("%s\001"%shop_on_review_num_level[review_num_level][shop_id]["show"])
      fp_w.write("%s\001"%shop_on_review_num_level[review_num_level][shop_id]["conv"])
  if review_num_level not in review_num_level_dict:
    fp_w.write("0\0010\001")
  else:
    fp_w.write("%s\001"%review_num_level_dict[review_num_level]["show"])
    fp_w.write("%s\001"%review_num_level_dict[review_num_level]["conv"])
  
  if review_position_rate not in shop_on_review_position_rate:
    fp_w.write("0\0010\001")
  else:
    if shop_id not in shop_on_review_position_rate[review_position_rate]:
      fp_w.write("0\0010\001")
    else:
      fp_w.write("%s\001"%shop_on_review_position_rate[review_position_rate][shop_id]["show"])
      fp_w.write("%s\001"%shop_on_review_position_rate[review_position_rate][shop_id]["conv"])
  if review_position_rate not in review_position_rate_dict:
    fp_w.write("0\0010\n")
  else:
    fp_w.write("%s\001"%review_position_rate_dict[review_position_rate]["show"])
    fp_w.write("%s\n"%review_position_rate_dict[review_position_rate]["conv"])

  if int(label) == -1:
    continue  
  if item_id not in item_dict:
    item_dict[item_id] = {"show":0,"conv":0}
  item_dict[item_id]["show"] += 1
  item_dict[item_id]["conv"] += int(label)
  if user_id not in user_dict:
    user_dict[user_id] = {"show":0, "conv":0}
  user_dict[user_id]["show"] += 1
  user_dict[user_id]["conv"] += int(label)
  if shop_id not in shop_dict:
    shop_dict[shop_id] = {"show":0, "conv":0}
  shop_dict[shop_id]["show"] += 1
  shop_dict[shop_id]["conv"] += int(label)
 
fp_w.close()     
