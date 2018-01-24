import pymysql
import pandas as pd

from website.settings import MPP_CONFIG


def from_sql_get_data(sql):
    # Connect to the database
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    try:
        res = corsor.fetchall()

        try:
            data = {"data": res, "heads": [x[0] for x in corsor.description]}
        except:
            data = None
    finally:
        ## connection.commit()
        corsor.close()
        connection.close()
    return data


## 单纯执行的
def sql_action(sql):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    # print(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return


from django.http import HttpResponse
# Create your views here.
def send_email(request):

    if request.method == 'POST':
        from django.core.mail import EmailMultiAlternatives
        getters = request.POST["mail_geters"].split(";")
        mail_content = str(request.POST["mail_content"])
        subject = '审计邮件|请求协助'
        msg = EmailMultiAlternatives(subject, mail_content, 'm13429888211@163.com', getters)
        msg.send()
        return HttpResponse("发送成功")

    if request.method == 'GET':
        s_id = request.session["eid"]
        e_id = int(str(s_id).split('opt')[1])

        from django.core.mail import EmailMultiAlternatives
        # print(request.GET["mail_geters"])
        getters = str(request.GET["mail_geters"]).split(";")
        getters.append("actanble@163.com")
        # print(getters)
        mail_content = request.GET["mail_content"]
        title = '代建局审计邮件|请求协助'
        # html_content = '<p>这是一封<strong>重要的</strong>邮件.</p>'
        msg = EmailMultiAlternatives(title, mail_content, 'actanble@163.com', getters)
        msg.content_subtype = "html"

        # 添加附件（可选）
        ### msg.attach_file('./twz.pdf')
        msg.send()

        s_id = request.session["eid"]
        e_id = int(str(s_id).split('opt')[1])
        extra_add = "向技术支持求助"
        from datetime import datetime
        params = {
            "event_stat": "求助",
            "event_time": str(datetime.today()),
            "extra_add": extra_add,
            "event_id": int(e_id),
            "opreater_name": request.user.username
            # "opreater_name": '网站管理员',
        }
        sql = """insert into proj_eventdetail(event_stat, event_time, extra_add, event_id, opreater_name) 
                            values('{event_stat}', '{event_time}', '{extra_add}', {event_id}, '{opreater_name}')""".format(
            **params)
        sql_action(sql)


        return HttpResponse("发送成功")


def get_stat_strings():
    return {
        "not_del": """<small class="label label-danger">未处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
        "done": """<small class="label label-default">已处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
        "ignore": """<small class="label label-warning">处理中</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
    }

#
# ### 批量处理函数 《---------服务于预警页面
# def gx(origin_df, res_strs, res_stats, i, del_df):
#     params = {
#         "rule_type": ["未知" if origin_df.loc[i, 'rules_type'] == None else origin_df.loc[i, 'rules_type']][0],
#         "src_ip": origin_df.loc[i, 'src_ip'],
#         "dst_ip": origin_df.loc[i, 'dst_ip'],
#         "start_time": origin_df.loc[i, 'start_time'],
#         "location": 'general',
#         "id": origin_df.loc[i, 'id'],
#     }
#     stat_lists = list(del_df[del_df['event_id'] == origin_df.loc[i, 'id']]["event_stat"])
#
#     if "完成" in stat_lists or "忽略" in stat_lists:
#         # temp_str = get_stat_strings()['done']
#         # res_strs.append(temp_str.format(**params))
#         # res_stats.append(3)
#         return res_strs, res_stats
#
#     if "签收" in stat_lists:
#         temp_str = get_stat_strings()['ignore']
#         res_strs.append(temp_str.format(**params))
#         res_stats.append(2)
#         return res_strs, res_stats
#
#     temp_str = get_stat_strings()['not_del']
#     res_strs.append(temp_str.format(**params))
#     res_stats.append(1)
#     return res_strs, res_stats


def judge_cate_from_ruleid(ruleid):
    ## 根据 rulemsg 判断
    s_ruleid = str(ruleid)
    first_word = {
        '9': '数据泄露',
    }
    forth_word = {
        '1': 'PMS',
    }
    if s_ruleid[3] in forth_word.keys():
        return forth_word[s_ruleid[3]]
    else:
        return '待分类'


def time_format(s):
    import re
    from datetime import datetime
    return datetime(*[int(x) for x in re.findall("""(.*?)-(.*?)-(.*?) (.*?):(.*?):(.*?)\.(.*)""", s)[0]])


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

#
# # 历史消息过滤
# def history_gl(origin_df, res_strs, res_stats, i, del_df):
#     head_strs = {
#         "not_del": """<small class="label label-danger">未处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
#         "done": """<small class="label label-default">已处理</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
#         "ignore": """<small class="label label-success">忽略</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
#         "is_del": """<small class="label label-warning">处理中</small>,{start_time}, {rule_type},{dst_ip},{src_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
#     }
#
#     params = {
#         "rule_type": ["未知" if origin_df.loc[i, 'rules_type'] == None else origin_df.loc[i, 'rules_type']][0],
#         "src_ip": origin_df.loc[i, 'src_ip'],
#         "dst_ip": origin_df.loc[i, 'dst_ip'],
#         "start_time": origin_df.loc[i, 'start_time'],
#         "location": 'general',
#         "id": origin_df.loc[i, 'id'],
#     }
#     stat_lists = list(del_df[del_df['event_id'] == origin_df.loc[i, 'id']]["event_stat"])
#
#     if "完成" in stat_lists:
#         temp_str = head_strs['done']
#         res_strs.append(temp_str.format(**params))
#         res_stats.append(3)
#         return res_strs, res_stats
#
#     if "忽略" in stat_lists:
#         temp_str = head_strs['ignore']
#         res_strs.append(temp_str.format(**params))
#         res_stats.append(2.5)
#         return res_strs, res_stats
#
#     if "签收" in stat_lists:
#         temp_str = head_strs['is_del']
#         res_strs.append(temp_str.format(**params))
#         res_stats.append(2)
#         return res_strs, res_stats
#
#     temp_str = head_strs['not_del']
#     res_strs.append(temp_str.format(**params))
#     res_stats.append(1)
#     return res_strs, res_stats
"""select id, rule_id, src_ip, dst_ip, t2.rules_type as rules_type  from 
                                user_alert 
                              left join (select sid, rules_type from regular) as t2
                                on user_alert.rule_id = t2.sid;"""