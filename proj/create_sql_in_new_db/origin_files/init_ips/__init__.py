import re
import pandas as pd
import pymysql
MPP_CONFIG = {
    'host': '192.168.0.110',
    'port': 9233,
    'user': 'root',
    'password': '112233..',
    'db': 'qydldb',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

## 单纯执行的
def sql_action(sql):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return


def get_datas():
    df = pd.read_csv('dj_init_ips.csv', encoding='utf-8')
    ips = df["ip"]
    names = df["app"]
    cates = df["cate"]
    res_indexs = []

    for x in range(len(ips)):
        if re.match('^\d+\.\d+\.\d+\.\d+$', str(ips[x])):
            res_indexs.append(x)

    res_datas = []
    for index in res_indexs:
        temp = {}
        temp.setdefault("ip", ips[index])
        temp.setdefault("belong_cate", cates[index])
        temp.setdefault("name", names[index])
        res_datas.append(temp)

    return res_datas

from datetime import datetime

def scripts_add_ip(data):
    params = {
        "ip": data["ip"],
        "name":  data["name"],
        "belongCate":data["belong_cate"],
        "tc_text": 'undefined',
        "add_date": datetime.today(),
        "area": '服务器区',
    }
    sql = """insert into proj_ipbelongarea(ip, name, belongCate, tc_text, add_date, area) 
                                    values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}')"""
    try:
        sql_action(sql.format(**params))
    finally:
        print("add_true")

if __name__=='__main__':
    import logging
    datas = get_datas()
    for data in datas:
        scripts_add_ip(data)
        logging.warning('have_write_data_to_sql!')

    print("end")