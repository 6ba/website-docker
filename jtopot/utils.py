###########################~！#######################################

def get_canvas_config2(canvas_width, canvas_height, fang):

    left_blank = float(canvas_width) * 0.137
    top_blank = float(canvas_height) * 0.067
    right_blank = float(canvas_width) * 0.168
    buttom_blank = float(canvas_height) * 0.147
    left_space = (float(canvas_width) - left_blank - right_blank)/(fang-1)
    top_space = (float(canvas_height) - top_blank - buttom_blank)/(fang-1)


    return {
        "fang": fang,
        "left_space": left_space,
        "top_space": top_space,
        "left_blank": left_blank,
        "top_blank": top_blank
    }


def get_canvas_config(canvas_width, canvas_height, fang):

    left_blank = float(canvas_width) * 0.1
    top_blank = float(canvas_height) * 0.1
    right_blank = float(canvas_width) * 0.15
    buttom_blank =  float(canvas_height) * 0.15
    left_space = (float(canvas_width) - left_blank - right_blank)/(fang-1)
    top_space = (float(canvas_height) - top_blank - buttom_blank)/(fang-1)


    return {
        "fang": fang,
        "left_space": left_space,
        "top_space": top_space,
        "left_blank": left_blank,
        "top_blank": top_blank
    }



def delow(data):
    ## 找到左上叫和右下叫两个变量, 再便便宜
    pass

def get_node_json(x, y, ip, text="", scalex=1, fo="0",img="djj1222/icon/server.png", textPosition="Bottom_Center", larm="undefined"):
    if text == "":
        text = int(x)*100 + int(y)
    return {
        "elementType": "node",
        "x": x,
        "y": y,
        "Image": img,
        "scaleX": scalex,
        "textPosition":textPosition,
        "larm": larm,
        "ip": ip,
        "text":text,
        "fo": fo,
        "id": int(x)*100 + int(y)
    }

def get_larm_node(temp_node, img1, img2, fo1, fo2, alfa):
    new_data = temp_node.copy()
    new_data["x"] = temp_node["x"] + 30 * alfa
    new_data["y"] = temp_node["y"] - 55 * alfa
    new_data["Image"] = img1
    new_data["text"] = ""
    new_data["fo"] = fo1
    temp = temp_node.copy()
    temp["Image"] = img2
    temp["ScaleX"] = 0.7
    temp["fo"] = fo2
    temp["text"] = ""
    return new_data, temp


def get_all_ips_info_based_dialog():
    from proj.utils import from_sql_get_data
    import pandas as pd

    ## 威胁预警
    sql = """select id, rule_id, src_ip, dst_ip, t2.rules_type as rules_type  from 
                                user_alert 
                              left join (select sid, rules_type from regular) as t2
                                on user_alert.rule_id = t2.sid;"""
    gjwx = from_sql_get_data(sql)["data"]

    ## 智能巡检
    sql2 = """select vulner_temp.vulner_name, vulner_temp.ip, vulner_temp.threat_code, eid_connect_cruiser_id.id as eid from vulner_temp 
                                      left join eid_connect_cruiser_id 
                                        on vulner_temp.uniq_id = eid_connect_cruiser_id.vulner_id
                                  ;"""
    znxj = from_sql_get_data(sql2)["data"]

    return gjwx, znxj

