## localhost -win86x64
# website目录下
..\..\..\venvs\venv\Scripts\activate.bat

## 远程链接mysql脚本
mysql -h192.168.0.110 -P9233 -uroot -p112233.. qldl201811
mysql -h10.1.203.99 -P32772 -uroot -proot qldl
mycli -h192.168.0.101 -uadmin007 -pmyadmin@816 qydldb
mysql -h10.1.203.99 -P9233 -uroot -proot -p112233.. qldl < demo_201818.sql
## 新加坡主机
mysql -h119.28.107.205 -P32768 -uroot -p112233..
# > CREATE DATABASE qydldb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
## 局域网主机备份数据库
mysql -h192.168.0.110 -P9233 -uroot -p112233.. qldl < qldl.sql
mysql -h119.28.107.205 -P32768 -uroot -p112233..
## 链接 redis
redis-cli -h192.168.0.110 -p1122 112233

## NOTE
- 处理表 proj_event_detail 预先不要为空。

## Docker 打包容器 [docker.io/actanble/site201811]
[http://www.linuxidc.com/Linux/2015-08/121184.htm]

## 打包本地数据库
> mysqldump -h192.168.0.101 -uadmin007 -pmyadmin@816 qydldb > demo_201818.sql

## docker 运行镜像
docker commit <c-id[:4]> actanble/dj-site
docker run -itd --net=host --cpu-period=100000 --cpu-quota=200000 --name dj_site actanble/dj-site