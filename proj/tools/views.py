from proj.utils import from_sql_get_data, judge_cate_from_ruleid


## 预警详情页右侧边栏
def deled_detail_by_eid(e_id):
    sql = """select t1.*, t2.* from (select * from proj_eventdetail where event_id={e_id}) as t2
                 left join
                (select id as no_use_id, start_time, rule_id, src_ip, dst_ip, t2.rules_type as rules_type  from
                    user_alert
                  left join (select sid, rules_type from regular) as t2
                        on user_alert.rule_id = t2.sid) as t1
                       on t1.no_use_id = t2.event_id;
                """.format(e_id=int(e_id))

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
            ## from .utils import judge_cate_from_ruleid

            event_desc = """{event_time}, src:{src_ip}, dst:{dst_ip}, {b_cate}, url:{event_ref}""".format(
                event_time=e["event_time"], src_ip=e["src_ip"], dst_ip=e['dst_ip'], b_cate='数据泄露', event_ref='待提取'
            )
            params = {
                "e_time": e["event_time"].time(),
                "event_cate": [judge_cate_from_ruleid(df["rule_id"][0])][0],
                "event_desc": event_desc,
                "extra_add": e['extra_add'],
                "event_name": event_desc,
                "opreater_name": e["opreater_name"],
                "event_stat": e["event_stat"]
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
                result_str += """<li><i class="fa bg-aqua"></i>
                                        <div class="timeline-item">
                                          <span class="time"><i class="fa fa-clock-o"></i> {e_time}</span>
                                          <h3 class="timeline-header"><a href="#">{event_cate}</a></h3>
                                          <h3>{event_stat}</h3>
                                          <div class="timeline-body">
                                            <strong>处理人:{opreater_name}</strong>
                                            </br>
                                            {extra_add}
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


## 预警详情页右侧边栏
def get_right_opt_info(e_id):
    sql = """select * from proj_eventdetail where event_id={e_id};""".format(e_id=int(e_id))

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
    first_day = True
    for day in new_days:
        result_str += """  <li class="time-label">
    				<span class="bg-green">
    				  {date}
    				</span>
    			  </li>""".format(date=day)

        if first_day:
            if int(e_id) < 10000000:
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
                  <span class="time"><i class="fa fa-clock-o"></i> {event_time}</span>
                  <h3 class="timeline-header no-border"><a href="#">安全主管</a> </h3>
                  <div class="timeline-body">
                    admin002:提醒网络管理员处理
                </div>
              </li>""".format(event_time=str(info["start_time"]), dst_ip=info["dst_ip"], src_ip=info["src_ip"])

            else:
                info = from_sql_get_data("""select t.* from 
                                        (select vulner_temp.*,eid_connect_cruiser_id.id as eid from vulner_temp 
                                                left join eid_connect_cruiser_id 
                                        on vulner_temp.uniq_id = eid_connect_cruiser_id.vulner_id) as t 
                                        where t.eid={};""".format(e_id))["data"][0]
                result_str += """<li>
                                        <i class="fa bg-aqua"></i>
                                        <div class="timeline-item">
                                          <span class="time"><i class="fa fa-clock-o"></i> {event_time}</span>
                                          <h3 class="timeline-header"><a href="#">智能巡检</a></h3>
                                          <div class="timeline-body">
                                            <strong>{src_ip}</strong>  <strong>{msg}</strong> 
                                          </div>
                                        </div>
                                      </li>
                                      <li>
                                    <i class="fa bg-aqua"></i>
                                    <div class="timeline-item">
                                      <span class="time"><i class="fa fa-clock-o"></i> {event_time}</span>
                                      <h3 class="timeline-header no-border"><a href="#">安全主管</a> </h3>
                                      <div class="timeline-body">
                                        superadmin:提醒网络管理员处理
                                    </div>
                                  </li>""".format(event_time=info["add_time"], sport=info["port"],
                                                  src_ip=info["ip"], msg=info["vulner_name"])
        first_day = False

        for e in [x for x in res_data if x["event_time"].date() == day]:
            params = {
                "event_time": e["event_time"].time(),
                "extra_add": e['extra_add'],
                "opreater_name": e["opreater_name"],
                "event_stat": e["event_stat"]
            }

            result_str += """<li>
                <i class="fa bg-aqua"></i>
                <div class="timeline-item">
                  <span class="time"><i class="fa fa-clock-o"></i>{event_time}</span>
                  <h3 class="timeline-header no-border"><a href="#">网络管理员</a> </h3>
                  <div class="timeline-body">
                    {opreater_name}:  {extra_add}
                  </div>
                </div>
              </li>""".format(**params)



    result_str += """<li>
        				<i class="fa fa-clock-o bg-gray"></i>
        			  </li>
        			</ul>
               """
    ## print(result_str)
    return result_str
