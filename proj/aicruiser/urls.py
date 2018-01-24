from django.conf.urls import url

from .views import *
from .abstracts import *
from .cruiser_history import *
from .vulner_task import *
from .user_opt import *
from .opt_add_script import events_ignore


urlpatterns = [
    # url(r'^aicruiser_init/$', aicruiser_init, name="proj_home"),
    # url(r'^aicruiser_lists/$', aicruiser_lists, name="aicruiser_lists"),
    url(r'^scanning_area/$', get_scanning_area, name="get_scanning_area"),
    url(r'^cruiser_home_info/$', cruiser_home_info, name="cruiser_home_info"),

    url(r'^vulner_lists/$', vulner_lists, name="vulner_lists"),
    url(r'^all_cruser_history/$', all_cruser_history, name="all_cruser_history"),
    url(r'^cruiser_task_detail/$', cruiser_task_detail, name="cruiser_task_detail"),

    ## 开始跟巡检任务设置有关
    url(r'^init_script/$', init_script, name="init_script"),
    url(r'^vulner_task_lists/$', vulner_task_lists, name="vulner_task_lists"),
    url(r'^task_prefor_list/$', task_prefor_list, name="task_prefor_list"),

    ## 开始和用户操作相关
    url(r'^add_task_to_cruiser/$', add_task_to_cruiser, name="add_task_to_cruiser"),
    url(r'^delete_task_by_id/$', delete_task_by_id, name="delete_task_by_id"),
    url(r'^update_task_checked/$', update_task_checked, name="update_task_checked"),
    url(r'^modify_task_by_id/$', modify_task_by_id, name="modify_task_by_id"),
    url(r'^cruiser_start/$', task_run_now, name="task_run_now"),

    ## 事件的批量忽略
    url(r'^events_ignore/$', events_ignore, name="events_ignore"),
]