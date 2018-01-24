"""
    本文件只能在实验环境的局域网中使用；其他无效;

        所以没有请求能够执行这个脚本！！！
"""
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

NEW_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '112233..',
    'db': 'qldl',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

## mycli -h192.168.0.101 -uadmin007 -pmyadmin@816 qydldb
CJW_CONFIG = {
    'host': '192.168.0.101',
    'port': 3306,
    'user': 'admin007',
    'password': 'myadmin@816',
    'db': 'qydldb',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}


def from_sql_get_data(sql, MPP_CONFIG):
    # Connect to the database
    connection = pymysql.connect(**MPP_CONFIG)
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
def sql_action(sql, MPP_CONFIG):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    # print(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return


import pandas as pd
def main(area):
    sql = "select * from jtopot_jips;"
    res = from_sql_get_data(sql, JTOPO_CONFIG)
    old_df = pd.DataFrame(list(res["data"]))
    ips = old_df["ip"]
    names = old_df["name"]
    print(ips)
    from datetime import datetime
    for i in range(len(ips)):
        import random
        tr = random.randint(1,100)
        cate = 'server'
        if tr > 70:
            cate = "host"
        params = {
            "ip": ips[i],
            "name": names[i],
            "belongCate": cate,
            "tc_text": 'undefined',
            "add_date": datetime.today(),
            "area": area,
        }
        insert_sql = """insert into proj_ipbelongArea(ip, name, belongCate, tc_text, add_date, area) 
                                        values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}')""".format(**params)
        sql_action(insert_sql, NEW_CONFIG)
        print("执行添加"+ ips[i] + ": " + names[i] + "成功！")

    print("全部成功")

def dump1():
    main('服务器区')


def dump_data_to_regular():
    orgin_datas = from_sql_get_data("""select rule_id, count(rule_id) from user_alert group by rule_id;""", CJW_CONFIG)["data"]
    rule_ids = pd.DataFrame(list(orgin_datas))["rule_id"]

    with open("F:\\all_datas_from_peryear\\beifen\\beifen_1207\\website\\proj\\create_sql_in_new_db\\origin_files\\demo.txt" , "r+", encoding="utf-8") as f:
        strs = f.readlines()
        f.close()

    attack_types = [str.split("\n")[0] for str in strs]
    for x in range(len(rule_ids)):
        params = {
            "sid": str(rule_ids[x]),
            "file_path": "f://own/private/res/data",
            "rules_type": attack_types[x],
            "attack_type": attack_types[x],
            "msg": "自己添加",
            "alarm_msg": "自己添加",
            "advice":"??????",
            "priority": 0,
            "actions": 10,
            "status": 9,
        }
        sql = """insert into regular(sid, file_path, rules_type, attack_type,msg,alarm_msg,advice,priority,actions,status) 
                            values('{sid}', '{file_path}', '{rules_type}','{attack_type}',
                            '{msg}','{alarm_msg}','{advice}',{priority},{actions},{status})""".format(
            **params)
        sql_action(sql, NEW_CONFIG)
        print("插入第 "+ str(x) +" 个成功！")

    get_sql_added = """select sid,file_path,alarm_msg,attack_type from regular where msg = "自己添加";"""
    ## 只有10个rule 我们新建几个有关系的rule_type 假的 sid



## dump_data_to_regular()


def set_new_data_into():
    """
    往user_alert 里面插入数据
    :return:
    """
    from datetime import datetime, timedelta
    rid = str(100)
    src_ip = '192.168.0.110'
    dst_ip = '112.232.43.55'
    params = {
        "start_time": datetime.today() - timedelta(minutes=5),
        "end_time": datetime.today() - timedelta(minutes=15),
        "rule_id": rid,
        "flow_id": "fow_id_no_any_other_use",
        "alert_times": 5,
        "src_ip": src_ip,
        'dst_ip': dst_ip,
        'ip_identifi_string': "no_any_that_use",
    }
    sql = """insert into user_alert(rule_id, start_time, end_time, flow_id, alert_times, src_ip, dst_ip, ip_identifi_string) 
                                values('{rule_id}','{start_time}', '{end_time}', '{flow_id}','{alert_times}',
                                '{src_ip}','{dst_ip}','{ip_identifi_string}')""".format(
        **params)
    sql_action(sql, NEW_CONFIG)
    # print("插入user_alert数据成功！")

# set_new_data_into()









