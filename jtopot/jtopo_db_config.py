
import pymysql
JTOPO_CONFIG = {
    'host': '192.168.0.110',
    'port': 9233,
    'user': 'root',
    'password': '112233..',
    'db': 'qlsj',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

def from_sql_get_data(sql):
    # Connect to the database
    connection = pymysql.connect(**JTOPO_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    try:
        res = corsor.fetchall()
        try:
            data = {"data": res, "heads": [x[0] for x in corsor.description]}
        except:
            data = None
    finally:
        ## connection.commit()
        corsor.close()
        connection.close()
    return data


## 单纯执行的
def sql_action(sql):
    connection = pymysql.connect(**JTOPO_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    # print(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return

