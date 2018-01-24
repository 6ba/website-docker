from django.http import JsonResponse, HttpResponse
from .utils import from_sql_get_data, sql_action

from datetime import datetime, time, timedelta
import pandas as pd
import re


def modify_task_by_id(request):
    t_id = int(request.GET["task_id"])

    request.session["modify_id"] = t_id
    # sql = """delete from cruiser_task_temp where id={};""".format(t_id)
    data = from_sql_get_data("""select * from cruiser_task_temp where id={}""".format(t_id))["data"][0]
    ## sql_action(sql)
    t_time = data["task_time"]
    hour,minute, second = str(t_time).split(":")
    run_onday = data["run_onday"]
    checked, month_day, week_day = '', '', ''
    if re.match('.*?天.*?', run_onday):
        checked = '每天'
    elif re.match('.*?月.*?', run_onday):
        checked = '每月'
        month_day = re.match("每月(\d+)号", run_onday).group(1)
    elif re.match('星期.*?', run_onday):
        checked = '每周'
        week_day = run_onday

    return JsonResponse({
        "task_time": data["task_time"],
        "task_desc": data["task_desc"],
        "hour": hour,
        "minute": minute,
        "checked": checked,
        "month_day":month_day,
        "week_day":week_day
    })


def delete_task_by_id(request):
    t_id = int(request.GET["task_id"])
    sql = """delete from cruiser_task_temp where id={};""".format(t_id)
    sql_action(sql)
    return HttpResponse("删除成功")


def insert_into_cruiser_factory(time, task_desc, single_checked, username):
    sql = """insert into cruiser_task_temp(task_time, task_desc, run_onday, used, created_user) 
              values('{task_time}', '{task_desc}', '{run_onday}', {used}, '{username}')"""

    params = {
        "task_time": str(time),
        "task_desc": task_desc,
        'run_onday': single_checked,
        "used": 1,
        "username":username,
    }
    sql_action(sql.format(**params))


def add_task_to_cruiser(request):
    if request.method == "POST":
        if "modify_id" in request.session:
            pre_delete_id = int(request.session["modify_id"])
            sql_action("""delete from cruiser_task_temp where id={};""".format(pre_delete_id))

        data = request.POST
        from datetime import time
        t_time = time(int(data["hour"]), int(data["minute"]), 0)
        task_desc = data["task_desc"]
        username = str(request.user.username)
        checked = data["checked"]
        single_checked = checked
        if checked == "每周":
            single_checked = data["week_day"]
        if checked == "每月":
            single_checked = "每月"+ str(data["month_day"]) + "号"

        # print(locals())
        if task_desc in from_sql_get_data("""select task_desc from cruiser_task_temp where run_onday='{run_onday}' and  task_time='{task_time}';""".format(
                run_onday=single_checked, task_time=str(t_time)))["data"]:
            # print("!!!!!!!!!!!!!!!!!!!!任务已经创建了!!!!!!!!!!!!!!!!!!!!!")
            return HttpResponse("任务已经有了")
        insert_into_cruiser_factory(t_time, task_desc, single_checked, username)

        return HttpResponse("创建任务成功")

"""更新checked按钮"""
# proj/update_task_checked/?task_checked=
def update_task_checked(request):
    t_id = int(request.GET["task_checked"].split("task_checked")[1])
    # stat = int(request.GET["task_stat"])
    data = from_sql_get_data("""select * from cruiser_task_temp where id={}""".format(t_id))["data"][0]
    inset_sql = """insert into cruiser_task_temp(task_time, task_desc, run_onday, used, created_user) 
                  values('{task_time}', '{task_desc}', '{run_onday}', {used}, '{username}')"""
    stat = [1 if data["used"] == 0 else 0][0]
    params = {
        "task_time": data["task_time"],
        "task_desc": data["task_desc"],
        'run_onday': data["run_onday"],
        "used": stat,
        "username": request.user.username,
    }
    sql_action("""delete from cruiser_task_temp where id={}""".format(t_id))
    sql_action(inset_sql.format(**params))
    action = "关闭"
    if (stat == 1):
        action = "开启"
    return HttpResponse(action+"按钮成功")

def begin_task(ips):
    import requests
    import json
    url = "http://localhost:6620/scantask"
    data = {
        'ips': ips,
        'ports': json.dumps({"T": "1-1023,E", 'U': "1-2048,8888,E"}),
        'user_id': 0x005,
        'scan_hash': '7B0D7D350A737B8B3C5813B63F39078B',
        'is_official': 0,
        'scan_aim': 1,
        'task_type': 1,
        'is_spawn': 0,
    }
    resp = requests.post(url, data=data)
    return resp

def task_run_now(request):
    ips = ",".join([x["ip"] for x in from_sql_get_data("""select ip from proj_ipbelongarea;""")["data"]])
    rep = begin_task(ips)
    return HttpResponse(rep)




