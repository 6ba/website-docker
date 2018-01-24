create_aicruser_table_sql = """
DROP TABLE IF EXISTS `self_cruiser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `self_cruiser` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT COMMENT '智能巡检消息唯一标识符',
  `start_time` datetime NOT NULL COMMENT '此条自检开始时间',
  `src_ip` varchar(15) NOT NULL,
  `sport` varchar(15) NOT NULL,
  `stat` varchar(15) NOT NULL COMMENT '此条状态|处理',
  `msg` varchar(50) NOT NULL COMMENT '消息',
  `level` varchar(20) NOT NULL DEFAULT '普通' COMMENT '等级',
  `sid` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
"""


from proj.utils import from_sql_get_data, sql_action

from datetime import datetime, timedelta

# arr=[
#     ["<small class=\"label label-danger\">高危紧急</small>","OS Detection Conseolidation and Reporting",
#               "192.168.0.4","general/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
#               ["<small class=\"label label-danger\">高危紧急</small>","高危端口",
#               "192.168.100.30","22/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
#               ["","重名账户",
#               "192.168.100.55","22/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
#               ["","用户信息残余",
#               "192.168.100.97","general/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
#               ["","默认共享开放",
#               "192.168.0.4","80/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
#     ]

arr=[["<small class=\"label label-danger\">高危紧急</small>","OS Detection Conseolidation and Reporting",
              "192.168.100.114","general/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
              ["<small class=\"label label-danger\">高危紧急</small>","高危端口",
              "192.168.100.120","22/tcp","<span class=\"badge bg-yellow\" name=\"sign\">处置</span>"],
    ]

def init_aicruser_db():
    delete_all_data_from_selfcruiser()
    dt = datetime.today() - timedelta(days=20)
    for i in range(len(arr)):
        dt += timedelta(days=2)
        level = "普通"
        if arr[i][0] != "":
            level = "高危"

        params = {
            "start_time": str(dt),
            "src_ip": arr[i][2],
            "sport": arr[i][3],
            "msg":arr[i][1],
            "stat": "发生",
            "level": level
        }
        sql = """insert into self_cruiser(start_time, src_ip, sport, msg, stat, level) VALUE('{start_time}','{src_ip}','{sport}','{msg}','{stat}','{level}')""".format(**params)
        sql_action(sql)

        print("插入fffffffff" + str(i))

def delete_all_data_from_selfcruiser():
    sql = """delete from  self_cruiser where id >222"""
    sql_action(sql)
    ##print("删除数据库")


if __name__ == '__main__':
    init_aicruser_db()
