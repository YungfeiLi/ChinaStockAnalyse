# -*- coding:utf-8 -*-

import os
import tushare as ts
import time
pro = ts.pro_api("fb14a04ff5cdae480ffcf2db551f15668a1c0bd5de1a137f4dde5b9a")


def get_date_list():
    date_list = []
    for i in range(2016, 2019):
        for j in range(1, 13):
            if j <= 9:
                date_element = "%d0%d01" % (i, j)
            else:
                date_element = "%d%d01" % (i, j)
            date_list.append(date_element)
    return date_list

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


def get_weight_data(code):
    date = get_date_list()
    for i in range(0, len(date)-1):
        start_date = date[i]
        end_date = date[i + 1]
        weight_data = pro.index_weight(index_code=code, start_date=start_date,end_date= end_date)
        time.sleep(0.5)

        path = "./data/weight_%s" % code
        mkdir(path)
        path = path + "/%s.csv" % start_date
        weight_data.to_csv(path)


if __name__ == "__main__":
    code = ["000001.sh","399001.sz","399300.sz"]
    for i in code:
        get_weight_data(i)
    print("所有的数据都已经下载在相应的文件夹中了，再见，朋友")