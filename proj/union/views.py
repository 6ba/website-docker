from django.http import HttpResponse, JsonResponse

from proj.utils import from_sql_get_data, sql_action
from datetime import datetime, timedelta


def init_opt():
    sql = """delete from proj_eventdetail where id>1"""
    sql_action(sql)


def init_user_alert():
    sql_action("""delete from user_alert where id > 1;""")

    arr2 = [
        ['222', '192.168.100.120', '47.28.90.111', "SQL注入攻击"],
        ['333', '192.168.100.114', '57.34.22.112', "网络扫描"],
        # ['44444', '192.168.100.120', '130.23.1.65', "发现MS17-010漏洞"],
    ]

    for i in range(len(arr2)):
        rid = arr2[i][0]
        src_ip = arr2[i][1]
        dst_ip = arr2[i][2]
        params = {
            "start_time": datetime.today() - timedelta(days=7),
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
        sql_action(sql)
        ## print("===============================")

def dump_data_to_regular():
    #### msg, alarm_msg, advice
    del_array2 = [
        # ["111", "系统SMB漏洞攻击", "获得系统权限、敏感数据泄露", "升级smb服务或者对系统打补丁"],
        ["222", "SQL注入攻击", "获取数据库数据、获得系统权限", "禁止此ip访问并修复注入点"],
        ["333", "网络扫描", "获取系统或web漏洞信息、获得主机权限、造成拒绝服务攻击", "禁止此ip访问或关闭不必要的端口"],
        ["444", "MS17-010漏洞", "获得系统权限、敏感数据泄露", "更新补丁"]
    ]

    sql_action("""delete from regular WHERE id>1;""")
    for x in range(len(del_array2)):
        params = {
            "sid": del_array2[x][0],
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
        ## print("插入第 "+ str(x) +" 个成功！")

    get_sql_added = """select sid,file_path,alarm_msg,attack_type from regular where msg = "自己添加";"""
    ## 只有10个rule 我们新建几个有关系的rule_type 假的 sid


#init_user_alert()
## dump_data_to_regular()


arr=[
    ["<small class=\"label label-danger\">高危紧急</small>", "MS17-010漏洞",
              "192.168.100.114", "general/tcp", "<span class=\"badge bg-yellow\" name=\"sign\">处置</span>", "444"],
    ]

def init_aicruser_db():
    sql_action("""delete from self_cruiser where id > 300;""")
    dt = datetime.today() - timedelta(days=20)
    for i in range(len(arr)):
        dt += timedelta(days=2)
        level = "普通"
        if arr[i][0] != "":
            level = "高危"

        params = {
            "start_time": str(dt),
            "src_ip": arr[i][2],
            "sport": arr[i][3],
            "msg":arr[i][1],
            "stat": "发生",
            "level": level,
            "sid": arr[i][5]
        }

        sql = """insert into self_cruiser(start_time, src_ip, sport, msg, stat, level, sid) VALUE('{start_time}','{src_ip}','{sport}','{msg}','{stat}','{level}','{sid}')""".format(**params)
        sql_action(sql)


