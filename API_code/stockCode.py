# -*- coding:utf-8 -*-

"""
This python file is a class to get the stock code and save them to the mysql.
"""

import tushare as ts
import pandas as pd
from sqlalchemy import create_engine

pro = ts.pro_api("******")


class stockCode:

    def __init__(self):
        pass

    def get_data(self, place):
        """
        this is a function that get the stock code from THSHARE.
        :param place: SSE上交所 SZSE深交所 HKEX港交所
        :return: a DataFrame of data
        """
        df = pro.query("stock_basic", exchange=place)
        data = pd.DataFrame(data=df, columns=["ts_code", "name", "industry"])
        return data

    def mysql_conn(self):
        """
        connect mysql
        :return: engine
        """
        engine = create_engine(
            'mysql+pymysql://root:******@127.0.0.1/******?charset=utf8')
        return engine

    def stockCodeAPI(self, pla):
        engine = self.mysql_conn()

        try:
            if pla == "sh":
                place = "SSE"
            elif pla == "sz":
                place = "SZSE"
            elif pla == "hk":
                place = "HKEX"
            else:
                print("输入错误")

            data = self.get_data(place)
            data.to_sql(pla + "_weight", engine, if_exists='append')
            print("股票代码导入完毕")
        except Exception as e:
            print(e)
            pass
