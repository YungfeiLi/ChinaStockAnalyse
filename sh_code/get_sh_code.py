# -*- coding:utf-8 -*-

import tushare as ts
import pandas as pd
from sqlalchemy import create_engine


def get_data():
    pro = ts.pro_api("fb14a04ff5cdae480ffcf2db551f15668a1c0bd5de1a137f4dde5b9a")
    df = pro.query("stock_basic", exchange="SSE")
    data = pd.DataFrame(data=df, columns=["ts_code", "name", "industry"])
    return data

def mysql_conn():
    engine = create_engine('mysql+pymysql://root:Lyf123..@127.0.0.1/chinastockanalyse?charset=utf8')
    return engine

if __name__ == "__main__":
    engine = mysql_conn()
    data = get_data()
    data.to_sql('sh_weight', engine, if_exists='append')