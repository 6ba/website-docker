# 模板文件记录

`task_d`   扫描任务记录   用户输入和设置扫描任务
`risk_d`   安全隐患列表
`risk_d_s` 安全隐患列表详情


# 表格处理备注
目前自检表有一个关联的整形ID; 每当表格进行创建写入之后, 执行一个关联脚本的产生

# NOTE
主要是记录巡检的相关内容


"""
import pymysql
import pandas as pd


MPP_CONFIG = {
    'host': '192.168.0.101',
    'port': 3306,
    'user': 'admin007',
    'password': 'myadmin@816',
    'db': 'qydldb',
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

def get_dt_by_time(current_dt, time_str):
    return datetime(*[int(x) for x in str(current_dt.date()).split("-")],
             *[int(x) for x in time_str.split(":")])

### 传进来一个最近的 dt 对象;
from datetime import datetime, timedelta
def get_pre_task_dts(last_dt):
    datas = from_sql_get_data("""select * from cruiser_task_temp;""")["data"]
    cn_week_days = ["日", "一", "二", "三", "四", "五", "六"]
    dts = []
    for data in datas:

        if data["run_onday"] == "每天":
            dts.append(get_dt_by_time(last_dt, str(data["task_time"])))
            dts.append(get_dt_by_time(last_dt + timedelta(days=1), str(data["task_time"])))

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
get_pre_task_dts(datetime(2018,1,5,9,0,0))

"""
