create_event_detail_sql = """
    DROP TABLE IF EXISTS `proj_eventdetail`;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!40101 SET character_set_client = utf8 */;
    CREATE TABLE `proj_eventdetail` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `event_id` int(11) NOT NULL,
      `event_stat` varchar(50) NOT NULL,
      `event_time` datetime(6) NOT NULL,
      `opreater_name` varchar(10) NOT NULL,
      `extra_add` longtext NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
    /*!40101 SET character_set_client = @saved_cs_client */;"""

create_IPbelongArea_sql = """
    DROP TABLE IF EXISTS `proj_ipbelongarea`;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!40101 SET character_set_client = utf8 */;
    CREATE TABLE `proj_ipbelongArea` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `ip` varchar(50) NOT NULL,
      `area` varchar(30) NOT NULL,
      `name` varchar(30) NOT NULL,
      `belongCate` varchar(20) NOT NULL,
      `tc_text` varchar(20) NOT NULL,
      `add_date` datetime(6) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

"""

opreaters_history_sql = """
    DROP TABLE IF EXISTS `proj_opreaters_history`;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!40101 SET character_set_client = utf8 */;
    CREATE TABLE `proj_opreaters_history` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `opreater_name` varchar(10) NOT NULL,
      `desc` varchar(20) NOT NULL,
      `opreate_time` datetime(6) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

"""

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
"""


set_eid_connect_cruiser_id = """
DROP TABLE IF EXISTS `eid_connect_cruiser_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eid_connect_cruiser_id` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '一千万开始自增的ID',
    `vulner_id` varchar(255) NOT NULL COMMENT '巡检表的ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
"""



"""
insert into proj_ipbelongarea(id, ip, name, belongCate, tc_text, add_date, area) 
                                values(60, '192.168.0.4', '主路由检查口', 'server','3 条告警信息','2017-12-11 11:23:03.828780', '服务器区');

insert into proj_ipbelongarea(id, ip, name, belongCate, tc_text, add_date, area) 
                                values(61, '192.168.0.4', '主路由检查口', 'server','1 条告警信息','2017-12-11 11:23:03.828780', '服务器区');

insert into proj_ipbelongarea(id, ip, name, belongCate, tc_text, add_date, area) 
                                values(60, '192.168.0.4', '主路由检查口', 'server','3 条告警信息','2017-12-11 11:23:03.828780', 'A栋');


insert into proj_ipbelongarea(id, ip, name, belongCate, tc_text, add_date, area) 
                                values(60, '192.168.0.4', '主路由检查口', 'server','3 条告警信息','2017-12-11 11:23:03.828780', '服务器区')

"""