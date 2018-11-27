# -*- coding:utf-8 -*-


import tushare as ts
import pymysql
import time

pro = ts.pro_api("fb14a04ff5cdae480ffcf2db551f15668a1c0bd5de1a137f4dde5b9a")


def conn():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="Lyf123..",
                           port=3306,
                           database="chinastockanalyse",
                           charset="utf8mb4")
    return conn


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


def get_date_weight(code, start_date, end_date):
    weight_data = pro.index_weight(
        index_code=code,
        start_date=start_date,
        end_date=end_date)
    return weight_data


def save_to_mysql(conn, data_origin, date):
    cursor = conn.cursor()
    time = "d" + date
    data = data_origin[['con_code', "weight"]]

    try:
        sql_create_col = "alter table sh_weight add %s float;" % time
        cursor.execute(sql_create_col)
    except Exception as e:
        print("该列已存在")
        pass

    for i in range(0, len(data)):
        try:
            ele = data.loc[i]
            con_code = ele[0]
            weight = float(ele[1])

            sql = "update sh_weight set %s=%f where ts_code = '%s';" % (
                time, weight, con_code)
            cursor.execute(sql)
            print("第%s条数据插入执行完毕" % i)
        except Exception as e:
            print(e)
            pass

    conn.commit()
    return None


def main(code):
    con = conn()

    date_list = get_date_list()

    for i in range(0, len(date_list)-1):
        start_date = date_list[i]
        end_date = date_list[i + 1]
        weight_data = get_date_weight(code=code, start_date=start_date,end_date= end_date)
        time.sleep(0.5)

        save_to_mysql(con, weight_data, start_date)


    print("所有数据均已储存")


if __name__ == "__main__":
    code = "000001.sh"
    main(code)