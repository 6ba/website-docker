from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def aicruiser_init(request):
    from .create_tables import init_aicruser_db
    init_aicruser_db()
    return HttpResponse("格式化成功")


def aicruiser_lists(request):
    from proj.utils import from_sql_get_data
    sql = """select * from self_cruiser;"""
    datas = from_sql_get_data(sql)["data"]

    res = []
    for i in range(len(datas)):
        temp = []
        if datas[i]["level"] == "高危":
            temp.append("<small class=\"label label-danger\">高危紧急</small>")
        else:
            temp.append("")
        temp.append(datas[i]["start_time"])
        temp.append(datas[i]["msg"])
        temp.append(datas[i]["src_ip"])
        temp.append(datas[i]["sport"])
        temp.append("""<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""".format(id=datas[i]["id"]))

        res.append(temp)

    return JsonResponse({'res': res})

import pandas as pd
def vulner_lists(request):
    from proj.utils import from_sql_get_data

    ## 设置当前最近的一个任务的信息; 完成度为100% 的最近的一个任务
    pre_sql = """select * from scan_task_temp 
                    where t_status=2 and t_ecode=0 and t_progress=100 and has_results > 0
                    order by t_update_time desc;"""
    current_ok_task = from_sql_get_data(pre_sql)["data"][0]
    task_id = current_ok_task["task_id"]

    sql = """select vulner_temp.*, t2.id as id 
                from (select * from vulner_temp where task_id = '{task_id}')as  vulner_temp
                left join eid_connect_cruiser_id as t2 
                    on vulner_temp.uniq_id = t2.vulner_id;""".format(task_id=task_id)
    datas = from_sql_get_data(sql)["data"]

    res = []
    for i in range(len(datas)):
        temp = []
        # NOte: 可以在这个位置增加上已完成处理等的标签; 目前省略掉了。
        if int(datas[i]["threat_code"]) > 1:
            temp.append("<small class=\"label label-danger\">高危紧急</small>")
        else:
            temp.append("")
        temp.append(datas[i]["add_time"])
        temp.append(datas[i]["vulner_name"])
        temp.append(datas[i]["ip"])
        temp.append(datas[i]["port"])
        temp.append("""<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""".format(id=datas[i]["id"]))

        res.append(temp)

    return JsonResponse({'res': res})
