import sys
import time

if len(sys.argv) < 3:
  print "Usage:python preprocessing.py train_log train_ins"
  exit(1)
fp_w = open(sys.argv[2], "w")
is_test = int(sys.argv[3])
#0:label 1:instance_id 2:item_id 3:item_category_list 4:item_property_list 5:item_brand_id 6:item_city_id 7:item_price_level 8:item_sales_level 9:item_collected_level 10:item_pv_level 11:user_id 12:user_gender_id 13:user_age_level 14:user_occupation_id 15:user_star_level 16:context_id 17:day 18:hour 19:context_page_id 20:predict_category_property 21:shop_id 22:shop_review_num_level 23:shop_review_positive_rate 24:shop_star_level 25:shop_score_service 26:shop_score_delivery 27:shop_score_description
property_list = ["3609861674619569089"]
item_dict = {}
shop_dict = {}
i = 0
for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split("\001")
  label = line[0]
  item_category_list = line[3].split(";")
  item_property_list = line[4].split(";")

  fp_w.write(raw_line.strip("\r\n") + "\001")
  item_property_set = set(item_property_list)
  fp_w.write("%s\001%s\001"%(len(item_category_list), len(item_property_set)))
  if len(item_category_list) == 2:
    fp_w.write("%s\001%s\001"%(item_category_list[1], -1))
  else:
    fp_w.write("%s\001%s\001"%(item_category_list[1], item_category_list[2]))
  
  item_id = line[2]
  shop_id = line[21]
  if item_id in item_dict:
    show = item_dict[item_id]["show"]
    conv = item_dict[item_id]["conv"]
    if show > 40:
      pcvr = 1.0 * conv / show
      show = 40
      conv = int(pcvr * 40)
      fp_w.write("%s\001"%(str(show)+"_"+str(conv)))
    else:
      fp_w.write("%s\001"%(str(show)+"_"+str(conv)))
  else:
    fp_w.write("0_0\001")
  if shop_id in shop_dict:
    show = shop_dict[shop_id]["show"]
    conv = shop_dict[shop_id]["conv"]
    if show > 40:
       pcvr = 1.0 * conv / show
       show = 40
       conv = int(pcvr * 40)
       fp_w.write("%s\n"%(str(show)+"_"+str(conv)))
    else:
      fp_w.write("%s\n"%(str(show)+"_"+str(conv)))
  else:
    fp_w.write("0_0\n")
  i+=1
  if is_test == 1:
    if i > 460138:
      continue
  else:
    if int(label) == -1:
      continue
  if item_id not in item_dict:
    item_dict[item_id] = {"show":0,"conv":0}
  item_dict[item_id]["show"] += 1
  item_dict[item_id]["conv"] += int(label)
  if shop_id not in shop_dict:
    shop_dict[shop_id] = {"show":0, "conv":0}
  shop_dict[shop_id]["show"] += 1
  shop_dict[shop_id]["conv"] += int(label)

fp_w.close()     
