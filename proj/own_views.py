from django.shortcuts import render
from django.http import HttpResponse
from .utils import from_sql_get_data
import pandas as pd


## 加载这些插件性能较差; 后期全部用运算缓存代替
def event_stat(request):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])

    user_oprete_data = from_sql_get_data("""select * from proj_eventdetail where event_id={};""".format(e_id))
    del_df = pd.DataFrame(list(user_oprete_data['data']))

    stat_lists = list(del_df['event_stat'])
    if "完成" in stat_lists:
        return HttpResponse(3)
    if "处理" in stat_lists:
        return HttpResponse(2)

    return HttpResponse(1)


def init_regular(request):
    from .union.views import dump_data_to_regular
    dump_data_to_regular()
    return HttpResponse("初始化 regular 数据库成功！")


from django.http import JsonResponse
def event_head_info(request):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])

    if e_id < 10000000:
        data = from_sql_get_data("""
                  select t1.*, regular.* from 
                     (select * from user_alert where id = {event_id}) as t1 
                      left join regular
                       on t1.rule_id = regular.sid""".format(event_id=e_id))[
            "data"][0]
        event_info = """<div>攻击方: {src_ip}</div> <div>被攻击方: {dst_ip}</div> </div>告警信息: {msg}</div> <div><strong>可能造成的危害:</strong></div></br><p>{abledange}</p>""".format(
            dst_ip=data["dst_ip"], src_ip=data["src_ip"], msg=data["msg"], abledange=data["alarm_msg"]
        )
        res = {
            "del_advice": data["advice"],
            "abledange": data["alarm_msg"],
            "event_info":event_info,
            "detail_head": '威胁预警详情',
            "area":"服务器区",
            "event_time": data["start_time"],
            "src_ip": data["src_ip"],
            "name": "??????????>>>><<<<<"
        }

        return JsonResponse({"res": res})
    ### 自检的
    data = from_sql_get_data("""select t2.* from (select vulner_temp.*, t2.id as id 
                  from vulner_temp
                left join eid_connect_cruiser_id as t2 
                    on vulner_temp.uniq_id = t2.vulner_id) as t2 where t2.id = {event_id};""".format(event_id=e_id))[
        "data"][0]
    event_info = """<div>主机: {src_ip}</div>  <div>告警: {msg}</div> <div>端口: {port}</div> <div><strong>可能造成的危害: </strong></div></br><p>{abledange}</p>""".format(
         src_ip=data["ip"], msg=data["vulner_name"], port=data["port"], abledange = data["vulnerability_desc_result"]
    )

    res = {
        "del_advice": data["solution"],
        "abledange": data["vulnerability_desc_result"],
        "event_info": event_info,
        "detail_head": '安全隐患详情',
        "area": "服务器区",
        "event_time": data["add_time"],
        "src_ip": data["ip"],
        "name": "??????????>>>><<<<<"
    }
    return JsonResponse({"res": res})



def init_all(request):
    # from .union.views import dump_data_to_regular, init_user_alert, init_opt, init_aicruser_db
    # ## 初始化 regular 规则表
    # dump_data_to_regular()
    # ## 初始化 user_alert 规则表
    # init_user_alert()
    # ## 初始化操作表格
    # init_opt()
    # ## 初始化漏洞表格
    # init_aicruser_db()

    return HttpResponse("初始化所有表格 OK!<<<<<--LOSE FUNC-->>>>>")


