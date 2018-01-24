from django.http import JsonResponse
from website.settings import MPP_CONFIG
from .utils import from_sql_get_data, get_stat_strings

class AbstractsJsonResponse():
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.key = kwargs.get(key)

import pandas as pd
# 威胁预警 | 威胁预警列表
def threat_warning_lists(request):
    # columns = ["时间", "攻击类型", "攻击", "被攻击", "location"]
    sql = """select t.*, proj_eventdetail.event_stat from 
                            (select id, start_time, rule_id, src_ip, dst_ip, alert_times, t2.rules_type as rules_type  from 
                            user_alert 
                          left join (select sid, rules_type from regular) as t2
                            on user_alert.rule_id = t2.sid) as t 
                    left join proj_eventdetail
                    on proj_eventdetail.event_id=t.id;"""
    datas = from_sql_get_data(sql)['data']

    user_alert_ids = np.unique([data["id"] for data in datas])
    res_strs, res_stats = [],[]
    for id in user_alert_ids:
        curent_id_datas = [data for data in datas if data["id"] == id]
        temp_data = curent_id_datas[0]
        params = {
            "rule_type": ["未知" if temp_data["rules_type"] == None else temp_data["rules_type"]][0],
            "src_ip": temp_data["src_ip"],
            "dst_ip": temp_data["dst_ip"],
            "start_time": temp_data["start_time"],
            "location": temp_data["alert_times"],
            "id": temp_data["id"],
        }

        if "签收" in [data["event_stat"] for data in curent_id_datas]:
            if "完成" in [data["event_stat"] for data in curent_id_datas] or "忽略" in [data["event_stat"] for data in curent_id_datas]:
                continue

            temp_str = get_stat_strings()['ignore']
            res_strs.append(temp_str.format(**params))
            res_stats.append(2)
            continue

        temp_str = get_stat_strings()['not_del']
        res_strs.append(temp_str.format(**params))
        res_stats.append(1)

    res_df = pd.DataFrame()
    res_df["stat"] = res_stats
    res_df["str"] = res_strs
    res_df = res_df.sort(columns=['stat'], ascending=True)

    return JsonResponse({'data': [x.split(',') for x in res_df["str"]]})


def sensitive_data_lists(request):
    sql = "select flowid, srcip, sport, dstip, ruleid, add_time from mtinfo;"
    res = from_sql_get_data(sql)
    df = pd.DataFrame(list(res['data']))
    new_df = pd.DataFrame()
    from .utils import judge_cate_from_ruleid
    new_df['时间'] = [str(x)[:4] + "/" +str(x)[4:6]+ "/" + str(x)[6:] for x in df["add_time"]]
    new_df['数据类型'] = [judge_cate_from_ruleid(rule_id) for rule_id in df["ruleid"]]
    new_df['泄漏源'] = df["srcip"]
    new_df['流向IP'] = df["dstip"]
    new_df['端口'] = df['sport']
    import numpy as np
    # print(df.to_json(orient='index'))
    # return JsonResponse({"data": df.to_json(orient='columns')})
    origin_array = np.array(new_df)
    res_array2 = [[origin_array[i][j] for j in range(len(origin_array[i]))] for i in range(len(origin_array))]
    return JsonResponse({"data": res_array2})


def threat_warning_history(request):
    head_strs = {
        "not_del": """<small class="label label-danger">未处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
        "done": """<small class="label label-default">已处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
        "ignore": """<small class="label label-success">忽略</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
        "is_del": """<small class="label label-warning">处理中</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
    }

    sql = """select t.*,proj_eventdetail.event_stat from (select id, start_time, rule_id, src_ip, dst_ip, alert_times, t2.rules_type as rules_type  from 
                                user_alert 
                              left join (select sid, rules_type from regular) as t2
                                on user_alert.rule_id = t2.sid) as t 
                        left join proj_eventdetail
                        on proj_eventdetail.event_id=t.id;"""
    datas = from_sql_get_data(sql)['data']

    user_alert_ids = np.unique([data["id"] for data in datas])
    res_strs, res_stats = [], []
    for id in user_alert_ids:
        curent_id_datas = [data for data in datas if data["id"] == id]
        temp_data = curent_id_datas[0]
        params = {
            "rule_type": ["未知" if temp_data["rules_type"] == None else temp_data["rules_type"]][0],
            "src_ip": temp_data["src_ip"],
            "dst_ip": temp_data["dst_ip"],
            "start_time": temp_data["start_time"],
            "location": temp_data["alert_times"],
            "id": temp_data["id"],
        }

        if "签收" in [data["event_stat"] for data in curent_id_datas]:
            if "完成" in [data["event_stat"] for data in curent_id_datas]:
                temp_str = head_strs['done']
                res_strs.append(temp_str.format(**params))
                res_stats.append(3)
                continue
            if "忽略" in [data["event_stat"] for data in curent_id_datas]:
                temp_str = head_strs['ignore']
                res_strs.append(temp_str.format(**params))
                res_stats.append(2.5)
                continue

            temp_str = head_strs['is_del']
            res_strs.append(temp_str.format(**params))
            res_stats.append(2)
            continue

        temp_str = head_strs['not_del']
        res_strs.append(temp_str.format(**params))
        res_stats.append(1)

    res_df = pd.DataFrame()
    res_df["stat"] = res_stats
    res_df["str"] = res_strs
    res_df["id"] = user_alert_ids
    res_df = res_df.sort(columns=['stat'], ascending=True)

    ignore_df = res_df[res_df["stat"] == 2.5]
    ignore_data = []
    ### print(list(ignore_df["id"]))
    for i in range(len(ignore_df)):
        re_ignore_str = """,<span class="label label-primary" onclick="re_ignore({eid})">取消忽略</span>""".format(eid=list(ignore_df["id"])[i])
        ignore_data.append((list(ignore_df["str"])[i] + re_ignore_str).split(','))
    return JsonResponse({
          'data': [x.split(',') for x in res_df["str"]],
         "ignore_data": ignore_data
        })

import numpy as np
def alert_home_info(request):
    ## 对于每一个 task_id 产生的数据进行整合分析;
    sql = """select user_alert.id,proj_eventdetail.event_stat from user_alert 
                left join proj_eventdetail on user_alert.id = proj_eventdetail.event_id;"""
    datas = from_sql_get_data(sql)["data"]
    all_ids = np.unique([data["id"] for data in datas])
    deling_ids = np.unique([data["id"] for data in datas if data["event_stat"] == "签收"])
    not_deled_ids = [id for id in all_ids if id not in deling_ids]
    deled_ids = np.unique([data["id"] for data in datas if data["event_stat"] == "忽略" or data["event_stat"] == "完成"])
    have_certied_ids = [id for id in all_ids if id not in deled_ids]

    return JsonResponse({"res": {
        "all_num": len(all_ids),
        "deling_ids": len(deling_ids),
        "not_deled_ids": len(not_deled_ids),
        "have_certied_ids": len(have_certied_ids)
    }})








