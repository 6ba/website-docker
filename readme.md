mysql:
    CREATE DATABASE `qydldb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

# python manage.py migrate 
python manage.py runserver


## 2018-1-18
> 修改首页展示顺序| jtopot/dj_views.py 首页返回的node节点按照告警显示

## 2018-1-19
> 修改时区 | 强制扭转

## 2018-1-22
> 修改首页按键关闭选项卡

## 待解决
- 1, df.sort(columns=['a', '-b'])
- 2, 修改task中的问题 | 已完成
- 3, 多进程数据库连接  | 略

## 2018-1-23
- 修改巡检任务出现的BUG（增加任务会重复）
- 修改巡检任务环节中 `cruiser_history` 出现的处理条目修改

## 2018-1-24
- 修改数据库写入状态的更新|不是重点
- 修改`CPU`占用 `--cpu-period=100000 --cpu-quota=200000`
- Find 目前两个数据库效率问题
- 1, user_alert.rule_id = regular.sid 联合查询是字符串联合, 查询极慢。
- 2, cruiser_task_temp.id = 关联表的 uniq_id 字符串联合, 查询略慢。


###########  END 
> collect_static 和 数据库 不公开。


