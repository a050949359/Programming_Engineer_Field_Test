import pymysql
import contextlib

check_where = "dns_sample where"

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

def registUser(account, password):
    with mysql() as cursor:
        sql = "insert into user (account, password) values ('{}', '{}');".format(account, password)
        try:
            cursor.execute(sql)
        except:
            return False

    with mysql() as cursor:
        sql = "SELECT account from user WHERE account = '{}';".format(account)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result["account"] == account:
            return True
        else:
            return False

def loginUser(account, password):
    with mysql() as cursor:
        sql = "SELECT account from user WHERE account = '{}' and password = '{}';".format(account, password)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            return False
        else:
            return True

def checkUser(account):
    with mysql() as cursor:
        sql = "SELECT account from user WHERE account = '{}';".format(account)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            print("失敗")
            return False
        else:
            print("成功")
            return True

def searchTime(date, time, usec, source_ip, fqdn):
    date_sql = ""
    time_sql = ""
    usec_sql = ""
    source_ip_sql = ""
    fqdn_sql = ""

    if date != "":
        date_sql = "date = '{}'".format(date)

    if time != "":
        time_sql = "time = '{}'".format(time)

    if usec != "":
        usec_sql = "usec = {}".format(usec)

    if source_ip != "":
        source_ip_sql = "source_ip = '{}'".format(source_ip)

    if fqdn != "":
        fqdn_sql = "fqdn like '{}%'".format(fqdn)

    with mysql() as cursor:
        where=False
        sql = "select DATE_FORMAT(date, '%Y-%m-%d') as date, DATE_FORMAT(time, '%H:%i:%s') as time, usec, source_ip, source_port, destination_ip, destination_port, fqdn from dns_sample"
        if date_sql != "":
            sql = sql + " where " + date_sql
            where=True
        
        if time_sql != "":
            if where:
                sql = sql + " and " + time_sql
            else:
                sql = sql + " where " + time_sql
                where=True

        if usec_sql != "":
            if where:
                sql = sql + " and " + usec_sql
            else:
                sql = sql + " where " + usec_sql
                where=True
        
        if source_ip_sql != "":
            if where:
                sql = sql + " and " + source_ip_sql
            else:
                sql = sql + " where " + source_ip_sql
                where=True

        if fqdn_sql != "":
            if where:
                sql = sql + " and " + fqdn_sql
            else:
                sql = sql + " where " + fqdn_sql
                where=True
        
        sql = sql + " order by date asc, time asc, usec asc;"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    
    return result

def searchBetweenTime(from_date, from_time, from_usec, to_date, to_time, to_usec, source_ip, fqdn):
    with mysql() as cursor:
        sql = "select DATE_FORMAT(date, '%Y-%m-%d') as date, DATE_FORMAT(time, '%H:%i:%s') as time, usec, source_ip, source_port, destination_ip, destination_port, fqdn from dns_sample"
        sql = buildSqlStrByDate(sql, from_date, to_date)
        sql = buildSqlStrByTime(sql, from_time, to_time)
        sql = buildSqlStrByUsec(sql, from_usec, to_usec)
        sql = buildSqlStrBySourceIp(sql, source_ip)
        sql = buildSqlStrByFQDN(sql, fqdn)
        sql = sql + " order by date asc, time asc, usec asc;"
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()

def buildSqlStrByDate(sql, from_date, to_date):
    if to_date == "" and from_date == "":
        return sql
    elif to_date == "":
        return sql + " where date = '{}'".format(from_date) if check_where not in sql else sql + " and date = '{}'".format(from_date)
    else:
        return sql + " where date between '{}' and '{}'".format(from_date, to_date) if check_where not in sql else sql + " and date between '{}' and '{}'".format(from_date, to_date)

def buildSqlStrByTime(sql, from_time, to_time):
    if to_time == "" and from_time == "":
        return sql
    elif to_time == "":
        return sql + " where time = '{}'".format(from_time) if check_where not in sql else sql + " and time = '{}'".format(from_time)
    else:
        return sql + " where time between '{}' and '{}'".format(from_time, to_time) if check_where not in sql else sql + " and time between '{}' and '{}'".format(from_time, to_time)

def buildSqlStrByUsec(sql, from_usec, to_usec):
    if to_usec == "" and from_usec == "":
        return sql
    elif to_usec == "":
        return sql + " where usec = {}".format(from_usec) if check_where not in sql else sql + " and usec = {}".format(from_usec)
    else:
        return sql + " where usec between {} and {}".format(from_usec, to_usec) if check_where not in sql else sql + " and usec between {} and {}".format(from_usec, to_usec)

def buildSqlStrBySourceIp(sql, source_ip):
    if source_ip == "":
        return sql
    else:
        return sql + " where source_ip = '{}'".format(source_ip) if check_where not in sql else sql + " and source_ip = '{}'".format(source_ip)

def buildSqlStrByFQDN(sql, fqdn):
    if fqdn == "":
        return sql
    else:
        return sql + " where fqdn like '{}%'".format(fqdn) if check_where not in sql else sql + " and fqdn like '{}%'".format(fqdn)
