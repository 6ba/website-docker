from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from proj.utils import from_sql_get_data, sql_action


def second_page_data(request):

    if request.method == "POST":
        sql = """select * from proj_ipbelongarea where area='{area}'""".format(area = request.session["area"])
        res = from_sql_get_data(sql)
        datas = res["data"]
        temp_data = []
        unique_ips = []
        for data in datas:
            if data["ip"] not in unique_ips:
                unique_ips.append(data["ip"])
                g_dict = {}
                g_dict.setdefault("ip", data["ip"])
                g_dict.setdefault("name", data["name"])
                g_dict.setdefault("tc_text", data["tc_text"])
                g_dict.setdefault("belongCate", data["belongCate"])

                temp_data.append(g_dict)
        fang = int(len(temp_data) ** (0.5)) + 1
        if abs((len(temp_data) ** (0.5)) - (int(len(temp_data) ** (0.5)))) < 0.0001:
            fang = int(len(temp_data)) ** 0.5

        ########## 根据当前情况创建 get_json ###data 里面记录Node信息
        data = []
        height, width = request.POST["canvas_height"], request.POST["canvas_width"]
        from proj.utils import get_canvas_config
        canvas_config = get_canvas_config(width, height, fang)
        ## fang = canvas_config["fang"]
        request.session["gj"] = {}
        request.session["xj"] = {}
        ## 告警和威胁全部设置为空的字典
        for index in range(len(temp_data)):
            lie = index % canvas_config["fang"]
            hang = int(index / canvas_config["fang"])

            img = ["server.png" if temp_data[index]["belongCate"] == "server" else "host.png"][0]
            larm = temp_data[index]["tc_text"]

            input_ip = temp_data[index]["ip"]
            all_mf = from_sql_get_data("select id,src_ip,dst_ip from user_alert where src_ip = '{ip}' and id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');".format(ip=input_ip))["data"]
            request.session["gj"].setdefault(input_ip, all_mf)
            larm = ["{num} 攻击威胁 ".format(num=len(all_mf)) if len(all_mf) > 0 else ""][0]

            wx_df = from_sql_get_data("select id,src_ip,msg,sport,level from self_cruiser where src_ip = '{ip}' and id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');".format(ip=input_ip))["data"]
            request.session["xj"].setdefault(input_ip, wx_df)
            larm += ["  {num} 安全隐患 ".format(num=len(wx_df)) if len(wx_df) > 0 else ""][0]

            if(len(all_mf) + len(wx_df) == 0):
                larm = "undefined"

            params = {
                "elementType": "node",
                "x": canvas_config["left_blank"] + canvas_config["left_space"] * lie,
                "y": canvas_config["top_blank"] + canvas_config["top_space"] * hang,
                "id": index + 1,
                "Image": img,
                "larm": larm,
                "scaleX": 1.3,
                "textPosition": "Bottom_Center",
                "text": temp_data[index]["name"],
                "ip": temp_data[index]["ip"],
            }
            data.append(params)

        return JsonResponse({"res": data, "fang": fang})


def factory_jip(request, sql, opreate):
    params = {
        "ip": request.GET["ip"],
        "name": request.GET["name"],
        "belongCate": request.GET["belongCate"],
        "tc_text": 'undefined',
        "add_date": datetime.today(),
        "area": request.session["area"],
    }

    try:
        sql_action(sql.format(**params))
    except:
        return HttpResponse(opreate + request.GET["ip"] + " 条目失败")

    # sql_action(sql.format(**params))
    return HttpResponse("已经" + opreate + request.GET["ip"] + " 条目")


#### 127.0.0.1:8000/jtopo/add_ip/?ip=192.168.111.1&stat=0&belongCate=server&tc_text=what001
def add_ip(request):
    if ip in from_sql_get_data('select ip from proj_ipbelongarea;')['data']:
        return HttpResponse("ip已经在其中了")
    sql = """insert into proj_ipbelongarea(ip, name, belongCate, tc_text, add_date, area) 
                                values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}')"""
    return factory_jip(request, sql, "添加")


def delete_ip(request):
    sql = "delete from proj_ipbelongarea where ip = '{ip}' and area = '{area}'".format(ip=request.GET["ip"], area=request.session['area'])
    try:
        sql_action(sql)
    except:
        return HttpResponse("删除" + request.GET["ip"] + " 条目失败")
    return HttpResponse("已删除" + request.GET["ip"] + " 条目")


def modify_ip(request):
    sql = """replace into proj_ipbelongarea(ip, name, belongCate, tc_text, add_date, area) 
                                values('{ip}', '{name}', '{belongCate}', '{tc_text}', '{add_date}', '{area}')"""
    return factory_jip(request, sql, "修改")


def get_area_name(request):
    if request.method == "POST":
        ## print(request.POST)
        request.session["area"] = request.POST["area_click"]
        return HttpResponse("<strong>" + request.session["area"] + "</strong> 区域概览")


def new_dialog(request):
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


def index_flash(request):
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



