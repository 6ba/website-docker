from django.http import JsonResponse, HttpResponse
from .utils import from_sql_get_data, sql_action

from datetime import datetime, time, timedelta
import pandas as pd
import numpy as np
import re

# from proj.user_opreations import event_functory

def ignore_event_factory(ip, type, username='script'):
    """
    :param username: 网页脚本操作员
    :param ip: 选择过滤的IP
    :param type: 智能巡检, 威胁预警
    :return: 操作结果和状态
    """
    if ip == 'all':
        eids = [data["id"] for data in from_sql_get_data("""select id from user_alert union all (select id from eid_connect_cruiser_id)""")["data"]]
    else:
        eids = np.unique([data["id"] for data in from_sql_get_data("""select t1.id from 
        (select id from user_alert where dst_ip='{ip}') as t1 
              union all 
            (select eid_connect_cruiser_id.id as id from 
                (select * from vulner_temp where ip = '{ip}') as  vulner_temp
             left join eid_connect_cruiser_id 
               on vulner_temp.uniq_id = eid_connect_cruiser_id.vulner_id)""".format(ip=ip))["data"]])
    get_param = lambda  eid, stat, extra_add : {
        "event_stat": stat,
        "event_time": str(datetime.today() + timedelta(seconds=28800)),
        "extra_add": extra_add,
        "event_id": int(eid),
        "opreater_name": username,
    }
    if type == 'wxyj':
        eids = [eid for eid in eids if eid < 10000000]
    elif type == 'znxj':
        eids = [eid for eid in eids if eid >= 10000000]
    else:
        pass
    for eid in eids:
        param_click = get_param(eid, "签收", "脚本签收")
        param_ignore = get_param(eid, "忽略", "脚本忽略")
        src_sql = """insert into proj_eventdetail(event_stat, event_time, extra_add, event_id, opreater_name) 
                            values('{event_stat}', '{event_time}', '{extra_add}', {event_id}, '{opreater_name}')"""
        if eid not in [data["event_id"] for data in from_sql_get_data("""select event_id from proj_eventdetail where event_stat='签收'""")["data"]]:
            sql_action(src_sql.format(**param_click))
        if eid not in [data["event_id"] for data in from_sql_get_data("""select event_id from proj_eventdetail where event_stat='忽略'""")["data"]]:
            sql_action(src_sql.format(**param_ignore))
    return "Have_done"

def events_ignore(request):
    ip = request.GET["ip"]
    type = request.GET["type"]
    try:
        username = request.user.username
    except:
        pass
    resp = ignore_event_factory(ip, type, username)
    return HttpResponse(resp)

