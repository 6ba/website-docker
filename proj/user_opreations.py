from django.http import JsonResponse, HttpResponse
from .utils import from_sql_get_data, sql_action

from datetime import datetime, timedelta
import pandas as pd
# from django.utils import timezone

def event_functory(request, stat, callback="您的处理已经提交", extra_add=""):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])

    params = {
        "event_stat": stat,
        "event_time": str(datetime.today() + timedelta(seconds=28800)),
        "extra_add": extra_add,
        "event_id": int(e_id),
        "opreater_name": request.user.username,

    }
    sql = """insert into proj_eventdetail(event_stat, event_time, extra_add, event_id, opreater_name) 
                    values('{event_stat}', '{event_time}', '{extra_add}', {event_id}, '{opreater_name}')""".format(
        **params)
    sql_action(sql)
    return HttpResponse("您的处理已经提交！")



def event_desolve(request):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])
    extra_add = request.GET["extra"]
    ## 判断同一个案件有没有再一分钟内连续处理
    # if not get_timestrap(request.user.username, e_id):
    #     return HttpResponse("不能30s内再次提交")

    return event_functory(request, "处理", extra_add=extra_add)


def event_click(request):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])
    ## 这个环节判断点击后，只签收一次，但是数据库效率较低
    sql = "select * from proj_eventdetail where event_id={e_id}".format(e_id=e_id)
    if len(from_sql_get_data(sql)["data"]) > 0:
        return HttpResponse("签收状态")
    return event_functory(request, "签收", extra_add="签收")


def event_done(request):
    return event_functory(request, "完成", "页面点击完成", "完成")


def event_ignore(request):
    return event_functory(request, "忽略", extra_add="忽略")


def event_detail_right(request):
    s_id = request.session["eid"]
    e_id = int(str(s_id).split('opt')[1])
    from .tools.views import deled_detail_by_eid, get_right_opt_info
    return HttpResponse(get_right_opt_info(e_id))


def get_timestrap(username, eid):
    now = datetime.today()
    sql = "select * from proj_eventdetail where event_id={eid};".format(eid=eid)
    df = pd.DataFrame(list(from_sql_get_data(sql)["data"]))
    if len(df) > 0:
        new_df = df[df["opreater_name"] == username]
        new_df = new_df.sort(["event_time"], ascending=True)
        from .utils import time_format
        last_time = time_format(str(new_df["event_time"][0]))
        if (now - last_time).seconds <= 30:
            return False
    return True


def index_flash(request):
    all_mf = from_sql_get_data("select * from user_alert where id not in (select event_id from proj_eventdetail);")["data"]
    num = len(all_mf)
    num2 = len(from_sql_get_data("select * from self_cruiser where id not in (select event_id from proj_eventdetail);")["data"])
    res_str_data_from_db = ""
    if num > 0:
        res_str_data_from_db += "发现{num}条攻击威胁".format(num=num)
    if num2 > 0:
        res_str_data_from_db += "发现{num2}条安全隐患".format(num2=num2)
    if num + num2 == 0:
        res_str_data_from_db = "undefined"
    res = {"res": [{"elementType":"node","x":115,"y":167,"id":19205,"Image":"newpics/1.png","scaleX":0.9000000000000001,"text":"网络和安全设备区","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":600,"y":167,"id":100200,"Image":"newpics/2.png","scaleX":0.9000000000000001,"text":"服务器区","textPosition":"Bottom_Center","larm":"3 条告警信息"},{"elementType":"node","x":107,"y":573,"id":61311,"Image":"newpics/3.png","scaleX":0.9000000000000001,"text":"A栋","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":747,"y":592,"id":442224,"Image":"newpics/4.png","scaleX":0.9000000000000001,"text":"食堂","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":172,"y":44,"id":7568,"Image":"newpics/5.png","scaleX":1.1,"text":"","textPosition":"Top_Center","larm":"undefined"},{"elementType":"node","x":434,"y":401,"id":174034,"Image":"newpics/6.png","scaleX":1.5,"text":"","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":417,"y":579,"id":241443,"Image":"newpics/3.png","scaleX":0.9000000000000001,"text":"B栋","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"link","nodeAid":7568,"nodeZid":19205,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":19205,"nodeZid":174034,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":100200,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":442224,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":61311,"nodeZid":174034,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":241443,"text":"","fontColor":"0, 200, 255"}]}
    for x in res["res"]:
        if x["text"] == "服务器区":
            x["larm"] = res_str_data_from_db
    ## 进入二级页面保存 cookie 后期在这里保存
    return JsonResponse(res)


def init_db_eventdetail(request):
    sql = """delete from proj_eventdetail where id>1"""
    sql_action(sql)
    return HttpResponse("初始操作数据库 ok")


def re_ignore(request):
    eid =  request.GET["eid"]
    sql = """delete from proj_eventdetail where event_id={} and event_stat = '忽略'""".format(int(eid))
    sql_action(sql)
    return HttpResponse("取消忽略成功")



