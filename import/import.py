import numpy as np
import pandas as pd
import pymysql
import contextlib
from datetime import datetime

# 定義上下文管理器，連線後自動關閉連線
@contextlib.contextmanager
def mysql(host='178.128.102.235', user='harold', passwd='123456', db='test_db'):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        
def insert_dns(df):
    sql = "insert into dns_sample(date, time, usec, source_ip, source_port, destination_ip, destination_port, fqdn) values('{}', '{}', {}, '{}', {}, '{}', {}, '{}');"
    with mysql() as cursor:
        for i in range(len(df.index)):
            date, time, usec = datetime.fromtimestamp(df.iloc[i]["frame.time_epoch"]).strftime("%Y-%m-%d,%H:%M:%S,%f").split(',')
            cursor.execute(sql.format(date, time, usec, df.iloc[i]["ip.src"], df.iloc[i]["udp.srcport"], df.iloc[i]["ip.dst"], df.iloc[i]["udp.dstport"], df.iloc[i]["dns.qry.name"]))

df = pd.read_csv('dns_sample.csv', sep=',')
df["dns.qry.name"] = df["dns.qry.name"] + "." + df["temp1"].fillna('') + "." + df["temp2"].fillna('')
df = df.drop(['temp1', 'temp2'], axis=1)
df["dns.qry.name"] = df["dns.qry.name"].map(lambda x: str(x).rstrip('.'))
df["udp.srcport"] = df["udp.srcport"].fillna(-1)
df["udp.dstport"] = df["udp.dstport"].fillna(-1)
insert_dns(df)

