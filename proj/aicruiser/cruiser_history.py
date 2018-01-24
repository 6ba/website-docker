from django.http import JsonResponse
import pandas as pd
import numpy as np

from proj.utils import from_sql_get_data

## 安全隐患信息列表
def all_cruser_history(request):

    ## 对于每一个 task_id 产生的数据进行整合分析;
    sql = """select t3.*,t4.t_add_time from(select t1.task_id, t1.eid, t1.threat_code, t2.event_stat from 
                                  (select vulner_temp.*,eid_connect_cruiser_id.id as eid from vulner_temp 
                                      left join eid_connect_cruiser_id 
                                        on vulner_temp.uniq_id = eid_connect_cruiser_id.vulner_id
                                  ) as t1 
                                  left join proj_eventdetail as t2 
                                      on t1.eid = t2.event_id
                                ) as t3
                            left join scan_task_temp as t4 
                               on t4.task_id=t3.task_id;"""

    datas = from_sql_get_data(sql)["data"]
    tasks = np.unique([data["task_id"] for data in datas])

    res_str_array = []
    for task_id in tasks:
        temp_task = [data for data in datas if data["task_id"] == task_id]
        if len(temp_task) == 0:
            continue
        task_dt = temp_task[0]["t_add_time"]
        all_terms_num = len(np.unique([x["eid"] for x in temp_task]))
        danger_terms_num = len([x for x in temp_task if x["threat_code"] > 1])
        ## 有签收状态代表处理中的总数
        lined_terms_num = len(np.unique([x["eid"] for x in temp_task if x["event_stat"] =="签收"]))
        deled_num = len(np.unique([x["eid"] for x in temp_task if x["event_stat"] =="忽略"
                                   or x["event_stat"] =="完成"]))
        params = {
            "task_dt": task_dt,
            "all_terms_num":all_terms_num,
            "danger_terms_num":danger_terms_num,
            "not_deled_num": all_terms_num - lined_terms_num,
            "task_id": task_id
        }

        if(all_terms_num - deled_num == 0):
            temp_str = """日常,{task_dt},{all_terms_num} 个隐患 {danger_terms_num} 个高危,
    <small class="label label-default">已处理</small>,<span class="badge bg-white" onclick="judge_to_risk_d_s('{task_id}')">查看</span>""".format(**params)
        else:
            ## 任务, 执行时间, 隐患数, 处理情况, 处置
            temp_str = """日常,{task_dt},{all_terms_num} 个隐患  {danger_terms_num} 个高危,
                <small class="label label-danger">{not_deled_num}个未处理</small>,<span class="badge bg-yellow" onclick="judge_to_risk_d_s('{task_id}')">处置</span>""".format(**params)

        res_str_array.append(temp_str.split(","))

    return JsonResponse({"res": res_str_array})


def cruiser_task_detail(request):
    ####### 生成 task_id -----
    task_id = request.session["task_id"]
    sql = """select t1.ip,t1.threat_code, t1.port, t1.vulner_name,t1.eid, t2.event_stat from 
                  (select vulner_temp.*,eid_connect_cruiser_id.id as eid from 
                        (select * from vulner_temp where task_id= '{task_id}') as vulner_temp
                      left join eid_connect_cruiser_id 
                        on vulner_temp.uniq_id = eid_connect_cruiser_id.vulner_id
                  ) as t1 
                  left join proj_eventdetail as t2 
                      on t1.eid = t2.event_id
                        """.format(task_id=task_id)
    datas = from_sql_get_data(sql)["data"]
    if(len(datas) == 0):
        return JsonResponse({"res": []})
    res_str_array=[]
    res_stats = []
    res_threat_codes = []

    eids = np.unique([data["eid"] for data in datas])
    for eid in eids:
        temp_data = [data for data in datas if data["eid"] == eid]
        if len(temp_data) == 0:
            continue
        if "签收" in [data["event_stat"] for data in temp_data]:
            if "完成" in [data["event_stat"] for data in temp_data] or "忽略" in [data["event_stat"] for data in temp_data]:
                del_stat = """<small class="label label-default">已处理</small>"""
                res_stats.append(3)
            else:
                del_stat = """<small class="label label-warning">处理中</small>"""
                res_stats.append(2)
        else:
            del_stat = """<small class="label label-danger">未处理</small>"""
            res_stats.append(1)

        res_threat_codes.append(int(temp_data[0]["threat_code"]))
        params = {
            "del_stat": del_stat,
            "vulner_name": temp_data[0]["vulner_name"],
            "safe_lever": int(temp_data[0]["threat_code"] * 33),
            "eid": temp_data[0]["eid"],
            "ip": temp_data[0]["ip"],
            "port": temp_data[0]["port"],
        }
        line_string="""{del_stat},
                        {vulner_name},
                    <div class="progress progress-xs">
                        <div class="progress-bar progress-bar-success" style="width: {safe_lever}%"></div>
                    </div>,
                  {ip},
                  {port},
                  <span class="badge bg-yellow" onclick="jump_to_detail('opt{eid}')">处置</span>""".format(**params)
        res_str_array.append(line_string.split(","))
    res_df = pd.DataFrame()
    res_df["stat"] = res_stats
    res_df["threat_code"] = res_threat_codes
    res_df["str"] = res_str_array
    res_str_df = res_df.sort(columns=['stat', "threat_code"], ascending=True)

    return JsonResponse({"res": list(res_str_df["str"])})


