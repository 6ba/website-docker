import pymysql

MPP_CONFIG = {
    'host': '192.168.0.101',
    'port': 3306,
    'user': 'admin007',
    'password': 'myadmin@816',
    'db': 'qydldb',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}
def from_sql_get_data(sql):
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
def sql_action(sql):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    # print(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return

def dump_false_data_to_regular():
    #### msg, alarm_msg, advice
    import numpy as np
    regular_sids  = np.unique([data["rule_id"] for data in from_sql_get_data("""select rule_id from user_alert;""")["data"]])
    del_array2 = [
        # ["111", "系统SMB漏洞攻击", "获得系统权限、敏感数据泄露", "升级smb服务或者对系统打补丁"],
        ["222222", "SQL注入攻击", "获取数据库数据、获得系统权限", "禁止此ip访问并修复注入点"],
        ["333", "网络扫描", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["333", "通用协议命令解码", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["333", "标准ICMP事件", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["333", "检测网络木马", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["333", "RPC解码查询", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["333", "大规模的信息收集", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
              # ["444", "MS17-010漏洞", "获得系统权限、敏感数据泄露", "更新补丁"]
    ]

    sql_action("""delete from regular WHERE id>285;""")
    print("删除初始默认增加的")
    for i in range(len(regular_sids)):
        x = i% (len(del_array2))
        params = {
            "sid": regular_sids[i],
            "file_path": "f://own/private/res/data",
            "rules_type": del_array2[x][1],
            "attack_type": del_array2[x][1],
            "msg": del_array2[x][1],
            "alarm_msg": del_array2[x][2],
            "advice":del_array2[x][3],
            "priority": 0,
            "actions": 10,
            "status": 9,
        }
        sql = """insert into regular(sid, file_path, rules_type, attack_type,msg,alarm_msg,advice,priority,actions,status) 
                            values('{sid}', '{file_path}', '{rules_type}','{attack_type}',
                            '{msg}','{alarm_msg}','{advice}',{priority},{actions},{status})""".format(
            **params)
        sql_action(sql)
        print("插入第 "+ str(i) +" 个成功！")

    get_sql_added = """select sid,file_path,alarm_msg,attack_type from regular where msg = "自己添加";"""
    ## 只有10个rule 我们新建几个有关系的rule_type 假的 sid


#init_user_alert()
dump_false_data_to_regular()
