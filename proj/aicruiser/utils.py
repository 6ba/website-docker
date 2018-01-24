from proj.utils import from_sql_get_data,sql_action
import pandas as pd

def get_uniq_ids_from_vulner(task_id):
    res_ids = pd.DataFrame(list(from_sql_get_data("""select * from vulner_temp where task_id=`{task_id}`};""".format(task_id=task_id))["data"]))["vulner_id"]
    return res_ids


def connect_eid_with_vulnerid_script(uniq_ids):
    for vulner_id in uniq_ids:
        try:
            sql = "insert into eid_connect_cruiser_id(`vulner_id`) VALUES ({vulner_id});".format(vulner_id=vulner_id)
            sql_action(sql)
        except:
            pass

def run_script():
    ts = pd.DataFrame(list(from_sql_get_data("""select * from scan_task_temp;""")["data"]))["task_id"]
    connect_eid_with_vulnerid_script(get_uniq_ids_from_vulner(ts[len(ts) - 1]))
    print("执行完成")


# 查询是否5min内可以执行
from datetime import datetime, time
def timetemp_is_in_five_minutes(pretime_str):
    now = datetime.now()
    pre_time_dt = datetime(*[int(x) for x in str(now.date()).split("-")], *[int(x) for x in pretime_str.split(":")])
    if abs((now - pre_time_dt).seconds) < 5*60:
        return True
    return False

def get_dt_by_time(current_dt, time_str):
    return datetime(*[int(x) for x in str(current_dt.date()).split("-")],
             *[int(x) for x in time_str.split(":")])

### 传进来一个最近的 dt 对象;
from datetime import datetime, timedelta
def get_pre_task_dts(last_dt):
    datas = from_sql_get_data("""select * from cruiser_task_temp where used = 1;""")["data"]
    cn_week_days = ["日", "一", "二", "三", "四", "五", "六"]
    dts = []
    for data in datas:
        if data["run_onday"] == "每天":
            y = lambda i: get_dt_by_time(last_dt + timedelta(days=i), str(data["task_time"]))
            test_days_in_a_eday = [y(i) for i in range(2) if  y(i) > last_dt]
            dts.extend(test_days_in_a_eday)

        ## 这里用了两个小技巧： 1全局设置调用本脚本模拟时间; 2,星期队列判断
        if len(data["run_onday"].split("星期"))>1:
            cn_current_weekday = data["run_onday"].split("星期")[1]
            gaim_week_day = [i for i in range(len(cn_week_days)) if cn_week_days[i] == cn_current_weekday][0]
            y = lambda i:get_dt_by_time(last_dt + timedelta(days=i), str(data["task_time"]))
            test_days_in_a_week = [y(i) for i in range(14) if y(i).weekday()==gaim_week_day and y(i)>last_dt]
            dts.extend(test_days_in_a_week)

        import re
        if re.match("""每月(\d+)号""", data["run_onday"]):
            gaim_day_num = int(re.findall("""每月(\d+)号""", data["run_onday"])[0])
            ## 遍历 `31` 天内 \d 号的日期集合
            y = lambda i: get_dt_by_time(last_dt + timedelta(days=i), str(data["task_time"]))
            test_days_in_a_month = [y(i) for i in range(31) if y(i).day == gaim_day_num and y(i) > last_dt]
            dts.extend(test_days_in_a_month)

    dts.sort()
    return dts
## run_srcipt()

