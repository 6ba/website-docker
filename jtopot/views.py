from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import os
from .jtopo_db_config import from_sql_get_data, sql_action
from datetime import datetime


################## 1133 记录; 版本0.4;
def yanshi(request):
    return render(request, "jtopot/demo/demo.html", {})


def factory_jip(request, sql, opreate):
    params = {
        "ip": request.GET["ip"],
        "name": request.GET["name"],
        "stat": 0,
        "belongCate": request.GET["belongCate"],
        "tc_text": '',
        "add_date": datetime.today()
    }

    try:
        sql_action(sql.format(**params))
    except:
        return HttpResponse(opreate + request.GET["ip"] + " 条目失败")

    # sql_action(sql.format(**params))
    return HttpResponse("已经" + opreate + request.GET["ip"] + " 条目")


#### 127.0.0.1:8000/jtopo/add_ip/?ip=192.168.111.1&stat=0&belongCate=server&tc_text=what001
def add_ip(request):
    sql = """insert into jtopot_jips(ip, name, stat, belongCate, tc_text, add_date) 
                                values('{ip}', '{name}', {stat}, '{belongCate}', '{tc_text}', '{add_date}')"""
    return factory_jip(request, sql, "添加")


def delete_ip(request):
    sql = "delete from jtopot_jips where ip = '{}'".format(request.GET["ip"])
    try:
        sql_action(sql)
    except:
        return HttpResponse("删除" + request.GET["ip"] + " 条目失败")
    return HttpResponse("已删除" + request.GET["ip"] + " 条目")


def get_get_modal(request):
    ip = request.GET["ip"]

    html = """
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">

                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <button type="button" class="btn btn-danger" onclick="delete_ip('""" + ip + """')" style="width:80px;float:right;">删除对象</button>
                <h4 class="modal-title" id="myModalLabel">IP信息修改 - <strong>""" + ip + """ </strong></h4>

            </div>

            <p><a href='http://roothan.com'>前往查看告警信息</a></p>
            <div id="msg" class="modal-body">  </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div>
            """

    return HttpResponse(html)


def lots_delete_ips(request):
    sql_action("delete from jtopot_jips where Id > 30;")
    return HttpResponse("批量删除尾部系统随机记录成功！")


def demo(request):
    return render(request, "jtopot/demo/second_page.html", {})


def index_jtopo(request):
    return render(request, "jtopot/jtopo_index.html", {})


def new_edit(request):
    return render(request, "jtopot/edit/index.html", {})


def test_index(request):
    return render(request, "jtopot/home_topo/index.html", {})


#####################智能编辑和存储#########################
def mongo_connect():
    from pymongo import MongoClient
    client = MongoClient('192.168.0.110', 27017)
    db = client.jtopo2
    collection = db.jtopo_jsons
    return collection


## 目前选用GET请求获取用户输入的Json数据
def add_json(request):
    if request.method == "POST":
        pass

    if request.method == "GET":
        import json
        temp_data = request.GET['jsonStr']
        ##print(json.loads(temp_data))

        temp_json = {
            "data": json.loads(temp_data),
            "add_time": datetime.today(),
            "datetype": "json",
            "location": "模拟图001",
            "input_type": "脚本添加",
        }

        mongo_connect().insert_one(temp_json)
        return HttpResponse("已经添加到后台")


### .sort({"add_time": -1})
def get_json(request):
    import json
    res = [x["data"] for x in mongo_connect().find()]
    res.reverse()
    return JsonResponse({"res": res[0]})


def get_all_json(request):
    import json
    res = {"data": [x["data"] for x in mongo_connect().find()]}
    return JsonResponse(res)


def show(request):
    return render(request, "jtopot/show.html", {})


def second_page(request):
    return render(request, "jtopot/second_page.html", {})


def get_canvas_size(request):
    alfa = 0.5
    size = {
        "canvas_height": int(request.GET["canvas_height"]) * alfa,
        "canvas_width": int(request.GET["canvas_width"]) * alfa
    }

    request.COOKIES["canvas_size"] = size
    #request.session["canvas_size"] = size
    return HttpResponse("已经获取画布大小")


def second_page_json(request):

    if request.method == "POST":
        sql = "select * from jtopot_jips;"
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
                g_dict.setdefault("stat", data["stat"])
                g_dict.setdefault("tc_text", data["tc_text"])
                g_dict.setdefault("belongCate", data["belongCate"])

                temp_data.append(g_dict)
        fang = int(len(temp_data) ** (0.5)) + 1
        if abs((len(temp_data) ** (0.5)) - (int(len(temp_data) ** (0.5)))) < 0.0001:
            fang = int(len(temp_data)) ** 0.5

        ########## 根据当前情况创建 get_json ###data 里面记录Node信息
        data = []
        height, width = request.POST["canvas_height"], request.POST["canvas_width"]
        from .utils import get_canvas_config
        canvas_config = get_canvas_config(width, height, fang)
        ## fang = canvas_config["fang"]
        for index in range(len(temp_data)):
            lie = index % canvas_config["fang"]
            hang = int(index / canvas_config["fang"])

            img = ["server.png" if temp_data[index]["belongCate"] == "server" else "host.png"][0]
            larm = [temp_data[index]["tc_text"] if temp_data[index]["stat"] == 1 else "undefined"][0]

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


from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponse


def upload(request):
    if request.method == "POST":
        try:
            text = handle_upload_file(request.FILES['file'], set_random_az9(5) + "___" + str(request.FILES['file']))
            ##request.session["push_text"] = text
            return HttpResponse(text)  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中

        except:
            return HttpResponse("文件格式错误;目前支持csv|txt")
    return HttpResponse("post文件")


def handle_upload_file(file, filename):
    path = 'upload/csv/'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)

    text = """"""
    with open(path + filename, 'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            text += chunk.decode('utf8')
    return text


def set_random_az9(n):
    seed = [x + 65 for x in range(26)]
    seed.extend([x + 97 for x in range(26)])
    seed.extend([x + 48 for x in range(10)])
    import random
    return "".join([str(chr(seed[random.randint(0, len(seed) - 1)])) for i in range(n)])


def edit_index(request):
    return render(request, "jtopot/home_edit.html", {})

def edit2(request):
    from proj.utils import sql_action,from_sql_get_data
    request.session["gj"] = {}
    request.session["xj"] = {}

    user_oprete_data = from_sql_get_data("""
            select t1.event_stat, user_alert.src_ip as gj_ip, t1.event_id as eid, self_cruiser.src_ip as zj_ip from
             (select * from proj_eventdetail) as t1 
               left join 
                user_alert 
               on t1.event_id = user_alert.id
               left join 
               self_cruiser 
               on t1.event_id = self_cruiser.id;""")["data"]
    import pandas as pd
    opt_df = pd.DataFrame(list(user_oprete_data))

    request.session["ip_stats"] = {}
    for input_ip in ["192.168.100.114", "192.168.100.120"]:
        all_mf = from_sql_get_data(
            "select id,src_ip,dst_ip from user_alert where src_ip = '{ip}' and id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');".format(
                ip=input_ip))["data"]
        request.session["gj"].setdefault(input_ip, all_mf)

        wx_df = from_sql_get_data(
            "select id,src_ip,msg,sport,level from self_cruiser where src_ip = '{ip}' and id not in (select event_id from proj_eventdetail where event_stat = '完成' or event_stat = '忽略');".format(
                ip=input_ip))["data"]
        request.session["xj"].setdefault(input_ip, wx_df)

        gj_df = opt_df[opt_df["gj_ip"] == input_ip]
        zj_df = opt_df[opt_df["zj_ip"] == input_ip]

        if(len(gj_df) + len(zj_df) == 0):
            request.session["ip_stats"].setdefault(input_ip, "未处理")
            continue

        all_event_id = pd.DataFrame((from_sql_get_data("""select id from user_alert where src_ip = '{ip}'
                                        union select id from self_cruiser where src_ip = '{ip}'""".format(ip=input_ip))["data"]))["id"]
        flag = False
        import numpy as np
        for id in [str(x) for x in all_event_id]:

            if(len(gj_df) >0 and int(id) < 10000):
                if (id not in gj_df[gj_df["event_stat"] == "完成"]["eid"]) and (id not in gj_df[gj_df["event_stat"] == "忽略"]["eid"]):

                    print(id)
                    print(list(gj_df[gj_df["event_stat"] == "完成"]["eid"]))
                    print(id in list(gj_df[gj_df["event_stat"] == "完成"]["eid"]))
                    flag = True
                    request.session["ip_stats"].setdefault(input_ip, "处理中")

            if (len(zj_df) > 0 and int(id) > 10000):
                if (id not in zj_df[zj_df["event_stat"] == "完成"]["eid"]) and (
                    id not in zj_df[zj_df["event_stat"] == "忽略"]["eid"]):
                    print("???? "+str(id))
                    print(zj_df)
                    flag = True
                    request.session["ip_stats"].setdefault(input_ip, "处理中")

        if not flag:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            request.session["ip_stats"].setdefault(input_ip, "完成")

    return render(request, "jtopot/edit2.html", {})


def canvas_size(request):
    return JsonResponse({"data": request.session["canvas_size"]})


def add_modal(request):

    pass


def test_contatiner(request):
    return render(request, "test_container.html", {})


def new_topo(request):
    return render(request, "jtopot/test1222.html")

from proj.utils import sql_action, from_sql_get_data
def test1222(request):


    return render(request, "jtopot/local_test1222.html")


def set_random_num8(request):
    import random
    try:
        a = request.GET["a"]
        res = [random.randint(1,8) for i in range(len(int(a))) if a>0]
    except:
        res = [random.randint(1,8) for i in range(12)]
    import numpy as np
    t= [1 for i in range(8)]
    for x in np.unique(res[:8]):
        t[x-1] = 0
    return JsonResponse({"res": t})


class Node():
    pass


def get_ips_stats(request):
    from proj.utils import from_sql_get_data, sql_action


def get_location_of_allnode(request):
    data = [{"elementType":"node","x":1009,"y":108,"id":108972,"Image":"djj1222/icon/server.png","scaleX":1.04,"text":"","textPosition":"Bottom_Center","larm":"2342434", "ip":"192.168.100.114", "fo": "0"},
             {"elementType":"node","x":892,"y":496,"id":446500,"Image":"djj1222/icon/server.png","scaleX":0.85,"text":"","textPosition":"Bottom_Center","larm":"222", "ip":"192.168.100.120", "fo": "0"}]



    db_data = {}
    db_data.setdefault("192.168.100.114", request.session["ip_stats"]["192.168.100.114"])
    db_data.setdefault("192.168.100.120", request.session["ip_stats"]["192.168.100.120"])


    if request.method == "POST":
        h = int(request.POST["canvas_height"])
        w = int(request.POST["canvas_width"])
        ## http://localhost:8000/jtopo/2?canvas_height=1500&canvas_width=900
        ## alfa = h/712
        alfax = w / 1250
        alfay = h / 712
        for i in range(len(data)):
            data[i]["x"] = data[i]["x"] * alfax
            data[i]["y"] = data[i]["y"] * alfay
            data[i]["scaleX"] = data[i]["scaleX"] * alfax
            if data[i]["larm"] != "undefined":
                data[i]["larm"] = "undefined"

            new_data = data[i].copy()

            if(db_data[new_data["ip"]] == "未处理"):
                new_data["x"] = data[i]["x"] + 30 * alfax
                new_data["y"] = data[i]["y"] - 55 * alfay
                new_data["Image"] = "djj1222/icon/mid_unread.png"
                new_data["fo"] = "1"
                temp = data[i].copy()
                temp["Image"] = "djj1222/icon/server_red.png"
                temp["fo"] = "1"
                data.append(temp)
                data.append(new_data)
            elif(db_data[new_data["ip"]] == "处理中"):
                new_data["x"] = data[i]["x"] + 30 * alfax
                new_data["y"] = data[i]["y"] - 55 * alfay
                new_data["Image"] = "djj1222/icon/mid_read.png"
                new_data["fo"] = "1"
                temp = data[i].copy()
                temp["Image"] = "djj1222/icon/server_orange.png"
                temp["fo"] = "1"
                data.append(temp)
                data.append(new_data)
            elif(db_data[new_data["ip"]] == "完成"):
                new_data["x"] = data[i]["x"] + 30
                new_data["y"] = data[i]["y"] - 55
                new_data["Image"] = "djj1222/icon/dealed.png"
                new_data["fo"] = "0"
                temp = data[i].copy()
                temp["Image"] = "djj1222/icon/server_blue.png"
                temp["fo"] = "1"
                data.append(temp)
                data.append(new_data)
            else:
                print("??????????????????????????????")

            data.append(new_data)


        return JsonResponse({"res": data})

def new_dialog(request):
    ip = request.GET["ip"]
    if "area" not in request.session.keys():
        request.session["area"] = "服务器区"
    sql = """select * from proj_ipbelongarea where area='{area}' and ip='{ip}';""".format(
        area=request.session["area"], ip=ip)
    res = from_sql_get_data(sql)
    element = res["data"][0]

    ######### 告警和威胁 #################
    gj = request.session["gj"]
    xj = request.session["xj"]

    if len(xj[ip]) == 0:
        res_aqyh_dialog = """无告警"""
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
            temp_str = """<tr><td>{index}</td>
                            <td>{event_level}</td>
                            <td>{event_msg}漏洞</td>
                            <td><i class="fa fa-gavel" name="gavel" id="opt{event_id}" onclick="jump_to_detail(this.id)"></i></td>
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
                                                    on t1.rule_id = regular.sid""".format(event_id=data["id"]))[
                "data"][0]["msg"]
            params = {
                "index": index,
                "src_ip": data["src_ip"],
                "dst_ip": data["dst_ip"],
                "event_id": data["id"],
                "event_type": event_type
            }

            temp_str = """<tr><td>{index}</td>
            <td>{event_type}</td>
            <td>
            <i class="fa fa-gavel" id="opt{event_id}" onclick="jump_to_detail(this.id)"></i>
            </td></tr>""".format(**params)

            res_gjwx_dialog += temp_str

    dialog_html = """<h5>当前区域:<span>""" + element["area"] + """</span></h5>
  <h5>名称:<span>""" + element["name"] + """</span></h5>
  <h5>IP:<span>""" + element["ip"] + """</span></h5>
  <h5>安全隐患</h5>
  <table class="table table-bordered table-striped">
    <tbody>
""" + res_aqyh_dialog + """
            </tbody>
          </table>
          <h5>攻击威胁</h5>
          <table class="table table-bordered table-striped gongji">
            <tbody>""" + res_gjwx_dialog + """</tbody></table>"""

    return HttpResponse(dialog_html)





