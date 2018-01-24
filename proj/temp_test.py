import pymysql
import pandas as pd
import numpy as np

MPP_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '112233..',
    'db': 'qldl',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}


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


def get_stat_strings():
    return {
        "not_del": """<small class="label label-danger">未处理</small>,{start_time}, {rule_type},{src_ip},{dst_ip},{location},<span class="badge bg-yellow" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">处置</span>""",
        "done": """<small class="label label-default">已处理</small>,{start_time}, {rule_type},{src_ip},{dst_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
        "ignore":"""<small class="label label-warning">忽略</small>,{start_time}, {rule_type},{src_ip},{dst_ip},{location},<span class="badge bg-default" name="sign" id="opt{id}" onclick="jump_to_detail(this.id)">查看</span>""",
    }

### 批量处理函数
def gx(origin_df, res_array2, i, del_df):
    params = {
        "rule_type": ["未知" if origin_df.loc[i, 'rules_type'] == None else origin_df.loc[i, 'rules_type']][0],
        "src_ip": origin_df.loc[i, 'src_ip'],
        "dst_ip": origin_df.loc[i, 'dst_ip'],
        "start_time": origin_df.loc[i, 'start_time'],
        "location": 'general',
        "id": origin_df.loc[i, 'id'],
    }

    if "完成" in list(del_df[del_df['event_id'] == origin_df.loc[i, 'id']]["event_stat"]):
        temp_str = get_stat_strings()['done']
        res_array2.append(temp_str.format(**params).split(","))
        return res_array2

    ## 必须再处理后才有忽略这个状态。。。
    if '处理' in list(del_df[del_df['event_id'] == origin_df.loc[i, 'id']]["event_stat"]):
        # print("fdsjlakfj !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        temp_str = get_stat_strings()['ignore']
        res_array2.append(temp_str.format(**params).split(","))
        return res_array2

    temp_str = get_stat_strings()['not_del']
    res_array2.append(temp_str.format(**params).split(","))

    return res_array2


import pandas as pd
# 威胁预警 | 威胁预警列表
def threat_warning_lists():
    columns = ["时间", "攻击类型", "攻击", "被攻击", "location"]
    sql = """select id, start_time, rule_id, src_ip, dst_ip, t2.rules_type as rules_type  from 
                        user_alert 
                      left join (select sid, rules_type from regular) as t2
                        on user_alert.rule_id = t2.sid;"""
    res = from_sql_get_data(sql)
    origin_df = pd.DataFrame(list(res['data']))

    ## 所有的事件初始产生存在 ID 就是发生状态; 当进行点击后就是签收; 才会产生后续的阶段
    user_oprete_data = from_sql_get_data("""select * from proj_eventdetail;""")
    del_df = pd.DataFrame(list(user_oprete_data['data']))
    ## del_ids = del_df['event_id']
    print(del_df)
    res_array2 = []
    for i in range(len(origin_df)):
        res_array2 = gx(origin_df, res_array2, i, del_df)

    print(del_df["event_id"])
    print(type(del_df["event_id"][2]))
    print(res_array2)
    print("""===========================================""")
    print(set(del_df[del_df['event_id']==190]["event_stat"]))





def judge_cate_from_ruleid(ruleid):
    ## 根据 rulemsg 判断
    s_ruleid = str(ruleid)
    first_word = {
        '9': '数据泄露',
    }
    forth_word = {
        '1': '交通',
    }
    if s_ruleid[3] in forth_word.keys():
        return forth_word[s_ruleid[3]]
    else:
        return '待分类'


def deled_detail_by_eid(e_id):
    sql = """select t1.*, t2.* from (select * from proj_eventdetail where event_id={e_id}) as t2
                 left join
                (select id as no_use_id, start_time, rule_id, src_ip, dst_ip, t2.rules_type as rules_type  from
                    user_alert
                  left join (select sid, rules_type from regular) as t2
                        on user_alert.rule_id = t2.sid) as t1
                       on t1.no_use_id = t2.event_id;
                """.format(e_id=int(e_id))
    # from event.views import from_sql_get_data
    res = from_sql_get_data(sql)
    res_data = res["data"]
    import pandas as pd
    df = pd.DataFrame(list(res_data))
    days = [x["event_time"].date() for x in res_data]
    ### 对 天数去重
    new_days = []
    for day in days:
        if day not in new_days:
            new_days.append(day)

    result_str = """"""
    result_str += """ <div class="box-body">
        			 <!-- The time line -->
        			<ul class="timeline">
        			  <!-- timeline time label -->
        			  """
    i = 0
    for day in new_days:
        result_str += """  <li class="time-label">
    				<span class="bg-green">
    				  {date}
    				</span>
    			  </li>""".format(date=day)

        for e in [x for x in res_data if x["event_time"].date() == day]:
            ## from .utils import judge_cate_from_ruleid

            event_desc = """{event_time}, src:{src_ip}, dst:{dst_ip}, {b_cate}, url:{event_ref}""".format(
                event_time = e["event_time"], src_ip = e["src_ip"], dst_ip=e['dst_ip'], b_cate='数据泄露', event_ref='待提取'
            )
            params = {
                "e_time": e["event_time"].time(),
                "event_cate": [judge_cate_from_ruleid(df["rule_id"][0])][0],
                "event_desc": event_desc,
                "extra_add": e['extra_add'],
                "event_name": event_desc,
                "opreater_name": e["opreater_name"]
            }
            if i == 0:
                result_str += """<li>
                        <i class="fa bg-aqua"></i>
                        <div class="timeline-item">
                          <span class="time"><i class="fa fa-clock-o"></i> {e_time}</span>
                          <h3 class="timeline-header"><a href="#">{event_cate}</a></h3>
                          <div class="timeline-body">
                            {event_name} <h3>发生</h3>
                            
                          </div>
                        </div>
                      </li>""".format(**params)
            else:
                result_str += """<li>
                                        <i class="fa bg-aqua"></i>
                                        <div class="timeline-item">
                                          <span class="time"><i class="fa fa-clock-o"></i> {e_time}</span>
                                          <h3 class="timeline-header"><a href="#">{event_cate}</a></h3>
                                          <div class="timeline-body">
                                            <strong>处理人:{opreater_name}</strong>
                                            </br>
                                            {extra_add}
                                          </div>
                                        </div>
                                      </li>""".format(**params)

            i += 1

    result_str += """
        			  <li>
        				<i class="fa fa-clock-o bg-gray"></i>
        			  </li>
        			</ul>
               </div><!-- /.box-body -->"""
    print(result_str)
    return result_str


# deled_detail_by_eid(190)


def event_stat():
    e_id = 190

    user_oprete_data = from_sql_get_data("""select * from proj_eventdetail where event_id={};""".format(e_id))
    del_df = pd.DataFrame(list(user_oprete_data['data']))
    if "完成" in del_df['event_stat']:
        return 3
    if "处理" in del_df['event_stat']:
        return 2

    return 1

##  print(event_stat())

def get_right_opt_info():
    e_id = 10005
    sql = """select t2.* from (select * from proj_eventdetail where event_id={e_id}) as t2""".format(e_id=int(e_id))

    res = from_sql_get_data(sql)
    res_data = res["data"]
    import pandas as pd
    df = pd.DataFrame(list(res_data))
    days = [x["event_time"].date() for x in res_data]
    ### 对 天数去重
    new_days = []
    for day in days:
        if day not in new_days:
            new_days.append(day)

    result_str = """"""
    result_str += """ <!-- The time line -->
        			<ul class="timeline">
        			  <!-- timeline time label -->
        			  """
    i = 0
    for day in new_days:
        result_str += """  <li class="time-label">
    				<span class="bg-green">
    				  {date}
    				</span>
    			  </li>""".format(date=day)

        for e in [x for x in res_data if x["event_time"].date() == day]:
            params = {
                "event_time": e["event_time"].time(),
                "extra_add": e['extra_add'],
                "opreater_name": e["opreater_name"],
                "event_stat": e["event_stat"]
            }
            if i == 0:
                if int(e_id) < 10000:
                    info = from_sql_get_data('select * from user_alert where id={}'.format(e_id))["data"][0]

                    result_str += """<li>
                        <i class="fa bg-aqua"></i>
                        <div class="timeline-item">
                          <span class="time"><i class="fa fa-clock-o"></i> {event_time}</span>
                          <h3 class="timeline-header"><a href="#">系统告警</a></h3>
                          <div class="timeline-body">
                            {dst_ip} 向 {src_ip} 跨域攻击
                          </div>
                        </div>
                      </li>
                      <li>
                    <i class="fa bg-aqua"></i>
                    <div class="timeline-item">
                      <span class="time"><i class="fa fa-clock-o"></i> { event_time }</span>
                      <h3 class="timeline-header no-border"><a href="#">安全主管</a> </h3>
                      <div class="timeline-body">
                        admin002:提醒网络管理员处理
                    </div>
                  </li>""".format(event_time=info["start_time"], dst_ip=info["dst_ip"], src_ip=info["src_ip"])

                else:
                    info = from_sql_get_data('select * from self_cruiser where id={};'.format(e_id))["data"][0]
                    print(info)
                    result_str += """<li>
                                            <i class="fa bg-aqua"></i>
                                            <div class="timeline-item">
                                              <span class="time"><i class="fa fa-clock-o"></i> {event_time}</span>
                                              <h3 class="timeline-header"><a href="#">智能巡检</a></h3>
                                              <div class="timeline-body">
                                                <strong>{src_ip}</strong> 自检发现 <strong>{sport}</strong> 有 <strong>{msg}</strong> 危险
                                              </div>
                                            </div>
                                          </li>
                                          <li>
                                        <i class="fa bg-aqua"></i>
                                        <div class="timeline-item">
                                          <span class="time"><i class="fa fa-clock-o"></i> { event_time }</span>
                                          <h3 class="timeline-header no-border"><a href="#">安全主管</a> </h3>
                                          <div class="timeline-body">
                                            admin002:提醒网络管理员处理
                                        </div>
                                      </li>""".format(event_time=info["start_time"], sport=info["sport"],
                                                      src_ip=info["src_ip"], msg=info["msg"])
            else:
                result_str += """<li>
                    <i class="fa bg-aqua"></i>
                    <div class="timeline-item">
                      <span class="time"><i class="fa fa-clock-o"></i>{event_time}</span>
                      <h3 class="timeline-header no-border"><a href="#">网络管理员</a> </h3>
                      <div class="timeline-body">
                        {opreater_name}:  {event_add}
                      </div>
                    </div>
                  </li>""".format(**params)

            i += 1

    result_str += """<li>
        				<i class="fa fa-clock-o bg-gray"></i>
        			  </li>
        			</ul>
               """
    ## print(result_str)
    return result_str



print(get_right_opt_info())
