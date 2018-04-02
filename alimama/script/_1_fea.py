#coding=utf-8
import sys
import time
import math

if len(sys.argv) < 3:
  print "Usage:python preprocessing.py train_log train_ins"
  exit(1)
fp_w = open(sys.argv[2], "w")
is_test = int(sys.argv[3])
#0:label 1:instance_id 2:item_id 3:item_category_list 4:item_property_list 5:item_brand_id 6:item_city_id 7:item_price_level 8:item_sales_level 9:item_collected_level 10:item_pv_level 11:user_id 12:user_gender_id 13:user_age_level 14:user_occupation_id 15:user_star_level 16:context_id 17:day 18:hour 19:context_page_id 20:predict_category_property 21:shop_id 22:shop_review_num_level 23:shop_review_positive_rate 24:shop_star_level 25:shop_score_service 26:shop_score_delivery 27:shop_score_description
item_dict = {}
shop_dict = {}

user_day_hour_dict = {}  
user_day_dict = {}
user_day_shop_dict = {}
user_day_item_dict = {}

item_day_hour_dict = {}
item_day_dict = {}

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split("\001")
  user_id = line[11]
  item_id = line[2]
  day = line[17]
  hour = line[18]
  shop_id = line[21]

  #一个用户一天每小时的展现量
  if day not in user_day_hour_dict:
    user_day_hour_dict[day] = {}
  if hour not in user_day_hour_dict[day]:
    user_day_hour_dict[day][hour] = {}
  if user_id not in user_day_hour_dict[day][hour]:
    user_day_hour_dict[day][hour][user_id] = {"show":0}
  user_day_hour_dict[day][hour][user_id]["show"] += 1
 
  #用户一天的展现量 
  if day not in user_day_dict:
    user_day_dict[day] = {}
  if user_id not in user_day_dict[day]:
    user_day_dict[day][user_id] = {"show":0}
  user_day_dict[day][user_id]["show"] += 1

  #用户一天看的某一个shop的次数
  if day not in user_day_shop_dict:
    user_day_shop_dict[day] = {}
  if user_id not in user_day_shop_dict[day]:
    user_day_shop_dict[day][user_id] = {}
  if shop_id not in user_day_shop_dict[day][user_id]:
    user_day_shop_dict[day][user_id][shop_id] = {"show":0}
  user_day_shop_dict[day][user_id][shop_id]["show"] += 1

  #用户一天看这个item次数  
  if day not in user_day_item_dict:
    user_day_item_dict[day] = {}
  if user_id not in user_day_item_dict[day]:
    user_day_item_dict[day][user_id] = {}
  if item_id not in user_day_item_dict[day][user_id]:
    user_day_item_dict[day][user_id][item_id] = {"show":0}
  user_day_item_dict[day][user_id][item_id]["show"] += 1

  #用户可能query的类别是否包括当前展现的item类别
  #用户可能query的属性和展现item的属性的于玄相似度
  #一个shop一天的展现数
  #一个shop一天一个小时的展现数
  #用户看过的这个item总数/用户看过的总的item总数
  #用户看过的这个shop总数/用户看过的总的shop总数

  #一个item一天一小时被展现的次数
  if day not in item_day_hour_dict:
    item_day_hour_dict[day] = {}
  if hour not in item_day_hour_dict[day]:
    item_day_hour_dict[day][hour] = {}
  if item_id not in item_day_hour_dict[day][hour]:
    item_day_hour_dict[day][hour][item_id] = {"show":0}
  item_day_hour_dict[day][hour][item_id]["show"] += 1

  #一个item一天被展现的次数
  if day not in item_day_dict:
    item_day_dict[day] = {}
  if item_id not in item_day_dict[day]:
    item_day_dict[day][item_id] = {"show":0}
  item_day_dict[day][item_id]["show"] += 1

user_day_query_item = {}
user_hist_query_item = {}
user_day_query_shop = {}
user_hist_query_shop = {}

for raw_line in open(sys.argv[1]):
  line = raw_line.strip("\n\r").split("\001")
  label = line[0]
  item_category_list = line[3].split(";")
  item_property_list = line[4].split(";")
  pre_cate_prop = line[20].split(";")
  prop = set()
  try:
    for cate_prop in pre_cate_prop:
      for p in cate_prop.split(":")[1].split(","):
        prop.add(p)
  except:
    pass
  fp_w.write(raw_line.strip("\r\n") + "\001")
  item_property_set = set(item_property_list)
  fp_w.write("%s\001%s\001"%(len(item_category_list), len(item_property_set)))
  if len(item_category_list) == 2:
    fp_w.write("%s\001%s\001"%(item_category_list[1], -1))
  else:
    fp_w.write("%s\001%s\001"%(item_category_list[1], item_category_list[2]))
  
  fp_w.write("%s\001%s\001"%(len(pre_cate_prop), len(prop)))  

  item_id = line[2]
  shop_id = line[21]
  user_id = line[11]
  day = line[17]
  hour = line[18]

  #item的历史转化率
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

  #user一天一小时的展现量
  if day in user_day_hour_dict:
    if hour in user_day_hour_dict[day]:
      if user_id in user_day_hour_dict[day][hour]:
        show = user_day_hour_dict[day][hour][user_id]["show"]
        fp_w.write("%s\001"%(show))
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")
  #uesr一天的展现量，分桶处理
  if day in user_day_dict:
    if user_id in user_day_dict[day]:
      show = user_day_dict[day][user_id]["show"]
      if show > 0 and show < 5:
        show = 1
      if show >=5 and show < 10:
        show = 2
      if show >=10 and show < 20:
        show = 3
      if show > 20:
        show = 4
      fp_w.write("%s\001"%(show))
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")
  #用户一天看的某个shop数
  if day in user_day_shop_dict:
    if user_id in user_day_shop_dict[day]:
      if shop_id in user_day_shop_dict[day][user_id]:
        show = user_day_shop_dict[day][user_id][shop_id]["show"]
        fp_w.write("%s\001"%(show))
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")
  #用户一天看的某一个item的数 
  if day in user_day_item_dict:
    if user_id in user_day_item_dict[day]:
      if item_id in user_day_item_dict[day][user_id]:
        show = user_day_item_dict[day][user_id][item_id]["show"]
        fp_w.write("%s\001"%(show))
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")

  if day in item_day_hour_dict:
    if hour in item_day_hour_dict[day]:
      if item_id in item_day_hour_dict[day][hour]:
        show = item_day_hour_dict[day][hour][item_id]["show"]
        if show >= 10:
          show = 10
        fp_w.write("%s\001"%show)
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")

  if day in item_day_dict:
    if item_id in item_day_dict[day]:
      show = item_day_dict[day][item_id]["show"]
      fp_w.write("%s\001"%show)
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")

  if user_id in user_day_query_item:
    if day in user_day_query_item[user_id]:
      if item_id in user_day_query_item[user_id][day]:
        fp_w.write("1\001")
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")
  
  if user_id in user_hist_query_item:
    if item_id in user_hist_query_item[user_id]:
        fp_w.write("1\001")
    else:
        fp_w.write("0\001")
  else:
      fp_w.write("0\001")
  
  if user_id in user_day_query_shop:
    if day in user_day_query_shop[user_id]:
      if shop_id in user_day_query_shop[user_id][day]:
        fp_w.write("1\001")
      else:
        fp_w.write("0\001")
    else:
      fp_w.write("0\001")
  else:
    fp_w.write("0\001")
  
  if user_id in user_hist_query_shop:
    if shop_id in user_hist_query_shop[user_id]:
        fp_w.write("1\001")
    else:
        fp_w.write("0\001")
  else:
      fp_w.write("0\001")

  #小时分桶处理
  if hour >= 0 and hour <= 6:
    fp_w.write("1\001")
  elif hour > 6 and hour <= 12:
    fp_w.write("2\001")
  elif hour > 12 and hour <= 18:
    fp_w.write("3\001")
  elif hour > 18 and hour <= 23:
    fp_w.write("4\001")
  else:
    fp_w.write("-1\001")  

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
  
  if user_id not in user_day_query_item:
    user_day_query_item[user_id] = {}
  if day not in user_day_query_item[user_id]:
    user_day_query_item[user_id][day] = set()
  user_day_query_item[user_id][day].add(item_id)

  if user_id not in user_hist_query_item:
    user_hist_query_item[user_id] = set()
  user_hist_query_item[user_id].add(item_id)

  if user_id not in user_day_query_shop:
    user_day_query_shop[user_id] = {}
  if day not in user_day_query_shop[user_id]:
    user_day_query_shop[user_id][day] = set()
  user_day_query_shop[user_id][day].add(shop_id)

  if user_id not in user_hist_query_shop:
    user_hist_query_shop[user_id] = set()
  user_hist_query_shop[user_id].add(shop_id)
  
  if is_test == 1:
    if line[17] == "24":
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
