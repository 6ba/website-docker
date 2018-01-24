"""关于自动化测试的文件———————— cruiser_task"""
"""字段描述:  任务描述_ task_desc, 任务设置时间 task_time, 日期 run_onday (星期, 每天, 几日), used 启用与否(0,1), """

create_sql = """DROP TABLE IF EXISTS `cruiser_task_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cruiser_task_temp` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT COMMENT 'unique_id_that_no_use',
  `task_time` time NOT NULL COMMENT 'task_time_in_one_day',
  `task_desc` varchar(15) NOT NULL COMMENT 'task describtion',
  `run_onday` varchar(15) NOT NULL COMMENT 'week|month|everyday',
  `used` int(2) unsigned NOT NULL COMMENT 'used_that_0|1' DEFAULT 0,
  `created_user` varchar(15) NOT NULL COMMENT '创建者_creater' DEFAULT 'admin002',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2018 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;"""

from django.http import HttpResponse, JsonResponse
from proj.utils import from_sql_get_data, sql_action


def init_script(request):
    """默认每天9点30和下午3点都有一次检查"""
    from datetime import time
    init_times = [time(9,30,0), time(15,0,0)]
    sql = """insert into cruiser_task_temp(task_time, task_desc, run_onday, used, created_user) 
          values('{task_time}', '{task_desc}', '{run_onday}', {used}, 'actanble')"""
    for time in init_times:
        params = {
            "task_time": str(time),
            "task_desc": '日常',
            'run_onday': "每天",
            "used": 1,
        }
        sql_action(sql.format(**params))

    return HttpResponse("初始化成功")


def vulner_task_lists(request):
    sql = """select * from cruiser_task_temp;"""
    datas = from_sql_get_data(sql)["data"]

    res_str_array = []
    for data in datas:
        check_stat = "unchecked"
        if int(data["used"]) > 0:
            check_stat = "checked"
        params = {
            "task_desc": data["task_desc"],
            "run_onday": data["run_onday"],
            "task_time": data["task_time"],
            "check_stat": check_stat,
            "id": data["id"]
        }

        temp_str = """{task_desc},
        {run_onday} {task_time},
        <input name="my-checkbox" type="checkbox" class="switch-small" {check_stat} id="task_checked{id}" />,
        <i class="fa fa-eyedropper ifir" onclick="modify_task_by_id({id})"></i>
        <i class="fa fa-remove isec" style="margin-left:20px;" onclick="delete_task_by_id({id})"></i>,
        {id}""".format(**params)
        res_str_array.append(temp_str.split(","))

    return JsonResponse({"res": res_str_array})

from datetime import datetime
def task_prefor_list(request):
    sql = """select * from (select * from scan_task_temp 
                    where t_status=2 and t_ecode=0
                    order by t_update_time desc limit 3)as t order by t_update_time;"""
    datas = from_sql_get_data(sql)["data"]
    res_table_tr_strs = """"""
    for data in datas:
        # temp_dt =  datetime(*[int(x) for x in str(data["t_update_time"]).split(" ")[0].split("-")],
        # *[int(x) for x in str(data["t_update_time"]).split(" ")[1].split(":")])
        temp_dt = data["t_update_time"]
        task_dt = str(temp_dt.month) + \
                  "月" + str(temp_dt.day) + \
                  "日" + " " + str(temp_dt.hour) + \
                  "." + str(temp_dt.minute)
        params = {
            "task_dt": task_dt,
            "task_progress": data["t_progress"],
        }
        temp_str = """<tr>
                    <td>{task_dt}</td>
                    <td>日常</td>
                    <td>
                      <div class="progress-bar" role="progressbar" aria-valuenow="{task_progress}"
                         aria-valuemin="0" aria-valuemax="100" style="width: {task_progress}%;">
                        <span class="">{task_progress}%</span>
                      </div>
                    </td>
                  </tr>""".format(**params)

        res_table_tr_strs += temp_str
    ## 首先在末尾装载两个 准备执行的任务
    from .utils import get_pre_task_dts
    for dt in get_pre_task_dts(datetime.now())[:2]:
        temp_str = """<tr>
                            <td>{task_dt}</td>
                            <td>日常</td>
                            <td>
                              <div class="progress-bar" role="progressbar" aria-valuenow="0"
                                 aria-valuemin="0" aria-valuemax="100" style="width: 0%;">
                                <span class="">0%</span>
                              </div>
                            </td>
                          </tr>""".format(task_dt=str(dt.month) + \
                  "月" + str(dt.day) + \
                  "日" + " " + str(dt.hour) + \
                  "." + str(dt.minute))
        res_table_tr_strs += temp_str

    return HttpResponse(res_table_tr_strs)







