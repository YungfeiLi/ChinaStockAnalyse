# -*- coding:utf-8 -*-

"""
This is a class that get the index weight from tushare and save them to mysql. For example, 000001.sh index weight.
"""

import tushare as ts
import pymysql
import time

# this is your tushare token.
pro = ts.pro_api("******")


class dataToMysql:

    def __init__(self):
        pass

    def conn(self):
        """
        this is the mysql database connection.
        :return: conn
        """
        conn = pymysql.connect(host="localhost",
                               user="root",
                               password="******",
                               port=3306,
                               database="******",
                               charset="utf8mb4")
        return conn

    def get_date_list(self):
        """
        this is a function that get the date list from 20160101 to 20181101.
        :return: date list
        """
        date_list = []
        for i in range(2016, 2019):
            for j in range(1, 13):
                if j <= 9:
                    date_element = "%d0%d01" % (i, j)
                else:
                    date_element = "%d%d01" % (i, j)
                date_list.append(date_element)
        return date_list

    def get_index_weight(self, code, start_date, end_date):
        """
        this is a function that get the index weight from tushare.
        :param code: the index code. for example:000001.sh
        :param start_date: start date, for example: 20160101
        :param end_date: end date, for example: 20180101
        :return: a pandas.DataFrame about index weight
        """
        weight_data = pro.index_weight(
            index_code=code,
            start_date=start_date,
            end_date=end_date)
        return weight_data

    def save_to_mysql(self, conn, data_origin, date, tb_name):
        """
        this is a function that save your index weight to mysql
        :param conn: pymysql connection
        :param data_origin: you origin data list. We will get useful information in it.
        :param date: get the date. For example,20180101
        :param tb_name: your mysql table name
        :return: None
        """
        cursor = conn.cursor()
        tim = "d" + date
        data = data_origin[['con_code', "weight"]]

        try:
            # create a column and save data.
            sql_create_col = "alter table %s add %s float;" % (tb_name, tim)
            cursor.execute(sql_create_col)
        except Exception as e:
            print(e)
            pass

        for i in range(0, len(data)):
            ele = data.loc[i]
            con_code = ele[0]
            weight = float(ele[1])

            sql = "update %s set %s=%f where ts_code = '%s';" % (
                tb_name, tim, weight, con_code)
            cursor.execute(sql)
            print("第%s条数据插入执行完毕" % i)

        try:
            conn.commit()  # execute command
            print("执行成功")
        except Exception as e:
            print(e)
            conn.rollback()

        return None

    def dataToMysql(self, code, table_name):
        """
        this is the execute function.
        :param code: index code. For example:000001.sh
        :param table_name: your mysql table name
        :return: None
        """
        # Here I have a setting, it is my mysql database connection.
        con = self.conn()

        date_list = self.get_date_list()

        for i in range(0, len(date_list) - 1):
            start_date = date_list[i]
            end_date = date_list[i + 1]
            weight_data = self.get_index_weight(
                code=code, start_date=start_date, end_date=end_date)
            time.sleep(0.5)

            self.save_to_mysql(
                conn=con,
                data_origin=weight_data,
                date=start_date,
                tb_name=table_name)

            print("日期%s所有数据均已储存" % start_date)

        print("所有数据均已经存储")
