from django.http import JsonResponse

from proj.utils import from_sql_get_data
import pandas as pd
import numpy as np


def get_scanning_area(request):
    sql = """select * from proj_ipbelongarea;"""
    datas = from_sql_get_data(sql)["data"]
    res = [[data["ip"], data["name"], data["area"], """<i class="fa faifir"></i> <i -eyedropper class="fa fa-remove isec" style="margin-left:20px;" onclick="delete_ip_from_topoarea('"""+ data["ip"] +"""')"></i>""", data["id"]] for data in datas]

    return JsonResponse({"res": res})


## 安全隐患信息列表
def cruiser_home_info(request):

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
    all_ids = np.unique([data["eid"] for data in datas])
    deling_ids = np.unique([data["eid"] for data in datas if data["event_stat"] == "签收"])
    not_deled_ids = [id for id in all_ids if id not in deling_ids]

    return JsonResponse({"res": {
        "all_num": len(all_ids),
        "deling_ids": len(deling_ids),
        "not_deled_ids": len(not_deled_ids),
    }})


