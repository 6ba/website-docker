from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from proj.utils import from_sql_get_data, sql_action


def factory_jip(request, sql, opreate):
    cateImg = "host"
    if "belongCate" in request.POST.keys():
        cateImg = request.POST["belongCate"]
    params = {
        "ip": str(request.POST["ip"]),
        "name": request.POST["name"],
        "belongCate": cateImg,
        "tc_text": 'undefined',
        "add_date": datetime.today(),
        # "area": request.session["area"],
        "area": request.POST["area"],
    }

    try:
        sql_action(sql.format(**params))
    except:
        return HttpResponse(opreate + params["ip"] + " 条目失败")
    # sql_action(sql.format(**params))
    return HttpResponse("已经" + opreate + params["ip"] + " 条目")


#### 127.0.0.1:8000/jtopo/add_ip/?ip=192.168.111.1&stat=0&belongCate=server&tc_text=what001
def add_ip(request):
    if request.method == "POST":
        if len(from_sql_get_data("""select * from proj_ipbelongarea where ip='{}'""".format(request.POST["ip"]))["data"]) > 0:
            return HttpResponse("该IP已经存在！")
        sql = """insert into proj_ipbelongarea(ip, name, belongCate, tc_text, add_date, area) 
                                    values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}')"""
        return factory_jip(request, sql, "增加")


def delete_ip(request):
    sql = "delete from proj_ipbelongarea where ip = '{ip}'".format(ip=request.GET["ip"])
    try:
        sql_action(sql)
    except:
        return HttpResponse("删除" + request.GET["ip"] + " 条目失败")
    return HttpResponse("已删除" + request.GET["ip"] + " 条目")


def modify_ip(request):

    sql = """delete from proj_ipbelongarea where ip = '{ip}';insert into proj_ipbelongarea(ip, name, belongCate, tc_text, add_date, area) 
                                values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}');"""
    return factory_jip(request, sql, "修改")


def get_area_name(request):
    if request.method == "POST":
        ## print(request.POST)
        request.session["area"] = request.POST["area_click"]
        return HttpResponse("<strong>" + request.session["area"] + "</strong> 区域概览")


def dj_topo_dialog(request):
    ip = request.GET["ip"]
    if "area" not in request.session.keys():
        request.session["area"] = "服务器区"
    sql = """select * from proj_ipbelongarea where area='{area}' and ip='{ip}';""".format(area = request.session["area"], ip=ip)
    res = from_sql_get_data(sql)
    element = res["data"][0]

    ######### 告警和威胁 #################
    gj = request.session["gj"]
    xj = request.session["xj"]

    if len(xj[ip]) == 0:
        res_aqyh_dialog =  """无告警"""
    else:
        temp_df_xj = xj[ip]
        res_aqyh_dialog = """"""
        index = 0
        for data in temp_df_xj:
            index += 1
            el = """"""
            if data["level"] == "高危":
                el = """<small class="label label-danger">高危紧急</small>"""
            params = {
                "index": index,
                "event_msg": data["msg"],
                "event_level": el,
                "event_id": data["id"],
            }
            temp_str = """<tr id="opt{event_id}" onclick="jump_to_detail(this.id)"><td>{index}</td>
                            <td>{event_level}</td>
                            <td>{event_msg}漏洞</td>
                            <td><i class="fa fa-gavel" name="gavel" ></i></td>
                      </tr>""".format(**params)
            res_aqyh_dialog += temp_str


    if len(gj[ip]) == 0:
        res_gjwx_dialog = """无告警"""
    else:
        res_gjwx_dialog = ""
        temp_df_wx = gj[ip]
        index = 0
        for data in temp_df_wx:
            index += 1
            event_type = from_sql_get_data("""select regular.* from 
                                                  (select * from user_alert where id = {event_id}) as t1 
                                                   left join regular
                                                    on t1.rule_id = regular.sid""".format(event_id=data["id"]))["data"][0]["msg"]
            params = {
                "index": index,
                "src_ip": data["src_ip"],
                "dst_ip": data["dst_ip"],
                "event_id": data["id"],
                "event_type": event_type
            }


            temp_str = """<tr id="opt{event_id}" onclick="jump_to_detail(this.id)"><td>{index}</td>
            <td>{event_type}</td>
            <td>
            <i class="fa fa-gavel" ></i>
            </td></tr>""".format(**params)

            res_gjwx_dialog += temp_str

    dialog_html = """<h5>当前区域:<span>"""+ element["area"] +"""</span></h5>
  <h5>名称:<span>"""+ element["name"] +"""</span></h5>
  <h5>IP:<span>"""+ element["ip"] +"""</span></h5>
  <h5>安全隐患</h5>
  <table class="table table-bordered table-striped">
    <tbody>
""" + res_aqyh_dialog + """
            </tbody>
          </table>
          <h5>攻击威胁</h5>
          <table class="table table-bordered table-striped gongji">
            <tbody>"""+ res_gjwx_dialog + """</tbody></table>"""


    return HttpResponse(dialog_html)


## 进入首页的时候 缓存这个信息大全; 再在session中获取
def index_topo_cache(request):
    all_mf = from_sql_get_data("select * from user_alert where id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');")["data"]
    num = len(all_mf)
    num2 = len(from_sql_get_data("select * from self_cruiser where id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');")["data"])
    res_str_data_from_db = ""
    if num > 0:
        res_str_data_from_db += "{num} 攻击威胁".format(num=num)
    if num2 > 0:
        res_str_data_from_db += " {num2} 安全隐患".format(num2=num2)
    if num + num2 == 0:
        res_str_data_from_db = "undefined"
    res = {"res": [{"elementType":"node","x":115,"y":167,"id":19205,"Image":"newpics/1.png","scaleX":0.9000000000000001,"text":"网络和安全设备区","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":600,"y":167,"id":100200,"Image":"newpics/2.png","scaleX":0.9000000000000001,"text":"服务器区","textPosition":"Bottom_Center","larm":"3 条告警信息"},{"elementType":"node","x":107,"y":573,"id":61311,"Image":"newpics/3.png","scaleX":0.9000000000000001,"text":"A栋","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":747,"y":592,"id":442224,"Image":"newpics/4.png","scaleX":0.9000000000000001,"text":"食堂","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":172,"y":44,"id":7568,"Image":"newpics/5.png","scaleX":1.1,"text":"","textPosition":"Top_Center","larm":"undefined"},{"elementType":"node","x":434,"y":401,"id":174034,"Image":"newpics/6.png","scaleX":1.5,"text":"","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"node","x":417,"y":579,"id":241443,"Image":"newpics/3.png","scaleX":0.9000000000000001,"text":"B栋","textPosition":"Bottom_Center","larm":"undefined"},{"elementType":"link","nodeAid":7568,"nodeZid":19205,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":19205,"nodeZid":174034,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":100200,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":442224,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":61311,"nodeZid":174034,"text":"","fontColor":"0, 200, 255"},{"elementType":"link","nodeAid":174034,"nodeZid":241443,"text":"","fontColor":"0, 200, 255"}]}
    for x in res["res"]:
        if x["text"] == "服务器区":
            x["larm"] = res_str_data_from_db
    ## 进入二级页面保存 cookie 后期在这里保存
    return JsonResponse(res)





