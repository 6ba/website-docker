from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import pandas as pd

from .utils import get_larm_node, get_node_json
from jtopot.utils import get_node_json
from proj.utils import from_sql_get_data


def home_edit():
    pass

#
# def json_dj_nodes(request):
#     if request.method == "POST":
#         res_json = []
#         w = int(request.POST["canvas_width"])
#         x = 1458 ### 第一个左上角的基于 `sd_w` 上的 x 位置
#         sd_w = 1824 ### 测试屏幕的大小
#         screen_xy_alfa = w / sd_w
#         y_of_ips = [267.7, 417.7, 583, 754, 932]
#
#         x_blace = 116 * screen_xy_alfa
#         for y in y_of_ips:
#             temp_3_json = [get_node_json(x=(x + x_blace*i) * screen_xy_alfa, y=y* screen_xy_alfa, ip=x) for i in range(3)]
#             res_json.extend(temp_3_json)
#
#         import pandas as pd
#         df1 = pd.DataFrame(list(res_json))
#         df1 = df1.sort(columns=['id'], ascending=True)
#
#         sql = """select ip,name from proj_ipbelongarea;"""
#         from proj.utils import from_sql_get_data
#         res_ips = from_sql_get_data(sql)["data"]
#         ips = [data["ip"] for data in res_ips]
#         temp_names = [data["name"] for data in res_ips]
#         names = [x[:5]+'..' if(len(x)>5) else x for x in temp_names]
#         res = []
#         from .utils import get_all_ips_info_based_dialog
#         wx, zj = get_all_ips_info_based_dialog()
#         request.session["ip_info"] = {}
#         # request.session["ip_stats"] = {}
#
#         opts = from_sql_get_data("""select * from proj_eventdetail;""")["data"]
#         import numpy as np
#         deling_ids = np.unique([data["event_id"] for data in opts if data["event_stat"] == "签收"])
#         deled_ids = np.unique([data["event_id"] for data in opts if data["event_stat"] == "忽略" or data["event_stat"] == "完成"])
#
#         """说明: 这里和上个版本相比; 省略了在模板渲染过程中产生session的过程; 这里一步到位"""
#         for index in range(len(ips[:15])):
#             ## 只显示前面的 id; //通过stats 监听，提示：：：后期根据闪烁的颜色判断即可
#             origin_node = df1[index:index+1]
#             new_node = get_node_json(x=list(origin_node["x"])[0], y=list(origin_node["y"])[0], ip=ips[index], text=names[index])
#
#             ## Dialog 设置session 缓存前面的
#             temp_json = {}
#             temp_wx = [data for data in wx if data["dst_ip"] == ips[index]]
#             temp_xj = [data for data in zj if data["ip"] == ips[index]]
#             temp_json.setdefault("wx", [data for data in temp_wx if data["id"] not in deled_ids])
#             temp_json.setdefault("xj", [data for data in temp_xj if data["eid"] not in deled_ids])
#             request.session["ip_info"].setdefault(ips[index], temp_json)
#             res.append(new_node)
#
#             ### 从这里开始准备节点的闪烁效果
#             from .utils import get_larm_node
#             current_ip_for_event_ids = [data["id"] for data in temp_wx if data["id"] not in deled_ids]
#             current_ip_for_event_ids.extend([data["eid"] for data in temp_xj if data["eid"] not in deled_ids])
#
#             current_ip_for_all_eids = [data["id"] for data in temp_wx]
#             current_ip_for_all_eids.extend([data["eid"] for data in temp_xj])
#             if len(current_ip_for_all_eids) > 0:
#                 if any([id in deling_ids for id in current_ip_for_event_ids]):
#                     node1, node2 = get_larm_node(new_node, "djj1222/icon/mid_read.png", "djj1222/icon/server_orange.png", "1", "1", screen_xy_alfa)
#                     res.append(node1)
#                     res.append(node2)
#                 else:
#                     if all([id in deled_ids for id in current_ip_for_all_eids]):
#                         # request.session["ip_stats"].setdefault(ips[index], "完成")
#                         node1, node2 = get_larm_node(new_node, "djj1222/icon/dealed.png", "djj1222/icon/server_blue.png", "0", "1", screen_xy_alfa)
#                         res.append(node1)
#                         res.append(node2)
#                     else:
#                         node1, node2 = get_larm_node(new_node, "djj1222/icon/mid_unread.png", "djj1222/icon/server_red.png", "1", "1", screen_xy_alfa)
#                         res.append(node1)
#                         res.append(node2)
#
#         return JsonResponse({"res": res})
#

def dj_ip_dialog(request):
    ip = request.GET["ip"]
    sql = """select * from proj_ipbelongarea where ip='{ip}';""".format(ip=ip)
    res = from_sql_get_data(sql)
    element = res["data"][0]

    ## 攻击威胁和智能巡检
    wx = request.session["ip_info"][ip]["wx"]
    xj = request.session["ip_info"][ip]["xj"]

    ## 先来巡检的
    if len(xj) == 0:
        res_aqyh_dialog = """无告警"""
    else:
        temp_df_xj = xj
        res_aqyh_dialog = """"""
        index = 0
        for data in temp_df_xj:
            index += 1
            el = """"""
            if data["threat_code"] > 1:
                el = """<small class="label label-danger">高危紧急</small>"""
            params = {
                "index": index,
                "event_msg": data["vulner_name"],
                "event_level": el,
                "event_id": data["eid"],
            }
            temp_str = """<tr id="opt{event_id}" onclick="jump_to_detail(this.id)"><td>{index}</td>
                                <td>{event_level}</td>
                                <td>{event_msg}漏洞</td>
                                <td><i class="fa fa-gavel" name="gavel" ></i></td>
                          </tr>""".format(**params)
            res_aqyh_dialog += temp_str

    ## 再来威胁预警的消息
    if len(wx) == 0:
        res_gjwx_dialog = """无告警"""
    else:
        res_gjwx_dialog = ""
        temp_df_wx = wx
        index = 0
        for data in temp_df_wx:
            index += 1
            params = {
                "index": index,
                "src_ip": data["src_ip"],
                "dst_ip": data["dst_ip"],
                "event_id": data["id"],
                "event_type": data["rules_type"]
            }

            temp_str = """<tr id="opt{event_id}" onclick="jump_to_detail(this.id)"><td>{index}</td>
                <td>{event_type}</td>
                <td>
                <i class="fa fa-gavel" ></i>
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

def get_nodes_positon(w, num_list_per_line):
    x = 1215  ### 第一个左上角的基于 `sd_w` 上的 x 位置
    sd_w = 1824  ### 测试屏幕的大小
    screen_xy_alfa = w / sd_w  ## 测试Canvas和显示Canvas宽度比
    y_of_ips = [184.7, 330.1, 489.7, 650.7, 848.7]  ## 竖着下来的五个的`y`坐标
    res_json = []
    x_blace = 120 * screen_xy_alfa  ## 每行间隔
    ## num_list_per_line = 5  ## 每行显示几个
    for y in y_of_ips:
        temp_3_json = [get_node_json(x=(x + x_blace * i) * screen_xy_alfa, y=y * screen_xy_alfa, ip=x) for i in range(num_list_per_line)]
        res_json.extend(temp_3_json)

    df1 = pd.DataFrame(list(res_json))
    df1 = df1.sort(columns=['id'], ascending=True)
    return  df1, screen_xy_alfa

### 首页节点产生图示
def json_dj_nodes(request):
    if request.method == "POST":

        w = int(request.POST["canvas_width"])
        num_list_per_line = 5
        ## IP 和 Name 关系的映射
        sql = """select ip,name from proj_ipbelongarea;"""
        from proj.utils import from_sql_get_data
        res_ips = from_sql_get_data(sql)["data"]
        ips = [data["ip"] for data in res_ips]
        temp_names = [data["name"] for data in res_ips]
        names = [x[:5] + '..' if (len(x) > 5) else x for x in temp_names]

        ## 开始记录达到Session过程的操作

        from .utils import get_all_ips_info_based_dialog
        wx, zj = get_all_ips_info_based_dialog()
        request.session["ip_info"] = {}
        opts = from_sql_get_data("""select * from proj_eventdetail;""")["data"]
        import numpy as np
        deling_ids = np.unique([data["event_id"] for data in opts if data["event_stat"] == "签收"])
        deled_ids = np.unique([data["event_id"] for data in opts if data["event_stat"] == "忽略" or data["event_stat"] == "完成"])

        """说明: 这里和上个版本相比; 省略了在模板渲染过程中产生session的过程; 这里一步到位"""
        res_stats = []
        for index in range(len(ips)):
            temp_json = {}
            temp_wx = [data for data in wx if data["dst_ip"] == ips[index]]
            temp_xj = [data for data in zj if data["ip"] == ips[index]]
            temp_json.setdefault("wx", [data for data in temp_wx if data["id"] not in deled_ids])
            temp_json.setdefault("xj", [data for data in temp_xj if data["eid"] not in deled_ids])
            request.session["ip_info"].setdefault(ips[index], temp_json)

            ### 从这里开始准备节点的闪烁效果
            from .utils import get_larm_node
            current_ip_for_event_ids = [data["id"] for data in temp_wx if data["id"] not in deled_ids]
            current_ip_for_event_ids.extend([data["eid"] for data in temp_xj if data["eid"] not in deled_ids])
            current_ip_for_all_eids = [data["id"] for data in temp_wx]
            current_ip_for_all_eids.extend([data["eid"] for data in temp_xj])

            if len(current_ip_for_all_eids) > 0:
                if any([id in deling_ids for id in current_ip_for_event_ids]):
                    ## 处理状态
                    res_stats.append(2)
                else:
                    if all([id in deled_ids for id in current_ip_for_all_eids]):
                        ## 完成状态
                        res_stats.append(1)
                    else:
                        ## 全部未处理
                        res_stats.append(3)
            else:
                ## 历史无隐患
                res_stats.append(0)

        df1, screen_xy_alfa = get_nodes_positon(w, num_list_per_line)
        res = res_delay_type(res_stats, df1, screen_xy_alfa, ips, names)
        return JsonResponse({"res": res})


## 根据 IP 对应的各个状态 重新绘图。
def res_delay_type(stats, df1, screen_xy_alfa, ips, names):
    res = []
    stat_df1 = pd.DataFrame()
    stat_df1["ip"] = ips
    stat_df1["stat"] = stats
    stat_df1["name"] = names
    res_stat_df = stat_df1.sort(columns=['stat'], ascending=False)
    # res_stat_df = stat_df1.sort_values(by='stat', ascending=False)
    # print(res_stat_df)
    ips = res_stat_df["ip"]
    names = res_stat_df["name"]
    show_num = 25
    i = 0
    for index in res_stat_df.index[:show_num]:

        origin_node = df1[i:i + 1]
        new_node = get_node_json(x=list(origin_node["x"])[0], y=list(origin_node["y"])[0], ip=ips[index], text=names[index], scalex=screen_xy_alfa)
        stat = res_stat_df["stat"][index]

        if stat == 2:
            node1, node2 = get_larm_node(new_node, "djj1222/icon/mid_read.png", "djj1222/icon/server_orange.png", "1", "1", screen_xy_alfa)
            res.extend([new_node, node1, node2])
        if stat == 1:
            node1, node2 = get_larm_node(new_node, "djj1222/icon/dealed.png", "djj1222/icon/server_blue.png", "0", "1", screen_xy_alfa)
            res.extend([new_node, node1, node2])
        if stat == 3:
            node1, node2 = get_larm_node(new_node, "djj1222/icon/mid_unread.png", "djj1222/icon/server_red.png", "1", "1", screen_xy_alfa)
            res.extend([new_node, node1, node2])
        if stat == 0:
            res.append(new_node)

        i += 1
    return res











