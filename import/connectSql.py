import pymysql
import contextlib

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
        
