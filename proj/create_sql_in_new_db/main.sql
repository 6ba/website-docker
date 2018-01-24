
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
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `proj_eventdetail` VALUES (1,10000,'脚本','2017-12-08 16:23:55.528077','网站管理员','范德萨范德萨范德萨范德萨发大水'),(2,302,'脚本','2017-12-18 15:08:27.415060','actanble','111111');

DROP TABLE IF EXISTS `proj_ipbelongarea`;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!40101 SET character_set_client = utf8 */;
    CREATE TABLE `proj_ipbelongarea` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `ip` varchar(50) NOT NULL,
      `area` varchar(30) NOT NULL,
      `name` varchar(30) NOT NULL,
      `belongCate` varchar(20) NOT NULL,
      `tc_text` varchar(20) NOT NULL,
      `add_date` datetime(6) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/DROP TABLE IF EXISTS `eid_connect_cruiser_id`;
*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eid_connect_cruiser_id` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '一千万开始自增的ID',
    `vulner_id` varchar(255) NOT NULL COMMENT '巡检表的ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/**触发器***/
DROP TRIGGER IF EXISTS t_afterinsert_on_valner_temp;
CREATE TRIGGER t_afterinsert_on_valner_temp
AFTER INSERT ON vulner_temp
FOR EACH ROW
BEGIN
     insert into eid_connect_cruiser_id(eid_connect_cruiser_id) values(new.vulner_temp_uniq_id);
END;