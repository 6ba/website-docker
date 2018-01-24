#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.homepage, name="proj_home"),
    url(r'^pages/intercept.html$', views.intercept, name="intercept"),
    url(r'^pages/logs.html$', views.logs, name="logs"),
    url(r'^pages/monitor.html$', views.monitor, name="monitor"),
    url(r'^pages/m.html$', views.m, name="m"),
    url(r'^pages/risk_d.html$', views.risk_d, name="risk_d"),
    url(r'^pages/warn_risk.html$', views.warn_risk, name="warn_risk"),
    url(r'^pages/risk_d_s.html$', views.risk_d_s, name="risk_d_s"),
    url(r'^pages/scanning.html$', views.scanning, name="scanning"),
    url(r'^pages/setting.html$', views.setting, name="setting"),
    url(r'^pages/setting1.html$', views.setting1, name="setting1"),
    url(r'^pages/setting2.html$', views.setting2, name="setting2"),
    url(r'^pages/setting3.html$', views.setting3, name="setting3"),
    url(r'^pages/souquan.html$', views.souquan, name="souquan"),
    url(r'^pages/task_d.html$', views.task_d, name="task_d"),
    url(r'^pages/voucher.html$', views.voucher, name="voucher"),
    url(r'^pages/voucher_all.html$', views.voucher_all, name="voucher_all"),
    url(r'^pages/voucher_in.html$', views.voucher_in, name="voucher_in"),
    url(r'^pages/voucher_out.html$', views.voucher_out, name="voucher_out"),
    url(r'^pages/warning.html$', views.warning, name="warning"),
    url(r'^pages/warningdetail.html$', views.warningdetail, name="warningdetail"),

    # url(r'^warning_detail/(?P<e_id>[0-9]+)/$', views.event_detail, name="warning_detail"),

]

from .abstracts import *
from .utils import send_email
from .user_opreations import *
from .own_views import event_stat, init_regular, event_head_info, init_all

abstract_urlparturns = [
    url(r'^threat_warning_lists/$', threat_warning_lists, name="threat_warning_lists"),
    url(r'^sensitive_data_lists/$', sensitive_data_lists, name="sensitive_data_lists"),
    url(r'^threat_warning_history/$', threat_warning_history, name="threat_warning_history"),
    url(r'^utils/send_email/$', send_email, name="send_email"),
    url(r'^user_event_click/$', event_click, name="event_click"),
    url(r'^user_event_ignore/$', event_ignore, name="event_ignore"),
    url(r'^user_event_reignore/$', re_ignore, name="re_ignore"),
    url(r'^user_event_complete/$', event_done, name="event_done"),
    url(r'^warning_del/$', event_desolve, name="warning_del"),
    url(r'^event_stat/$', event_stat, name="event_stat"),
    url(r'^event_detail_right/$', event_detail_right, name="event_detail_right"),
    url(r'^event_head_info/$', event_head_info, name="event_head_info"),
    ### 两个初始化的表格
    url(r'^opt_init/$', init_db_eventdetail, name="init_db_eventdetail"),
    url(r'^alert_home_info/$', alert_home_info, name="alert_home_info"),
    url(r'^regular_init/$', init_regular, name="init_regular"),
    url(r'^init_all/$', init_all, name="init_all"),
]

urlpatterns += abstract_urlparturns

from .union.topo_view import get_area_name, delete_ip, add_ip, modify_ip, second_page_data, new_dialog, index_flash
opreaters_urlparterns = [
    url(r'^get_area_name/$', get_area_name, name="get_area_name"),
    url(r'^add_ip/$', add_ip, name="add_ip"),
    url(r'^delete_ip/$', delete_ip, name="delete_ip"),
    url(r'^get_area_name/$', modify_ip, name="modify_ip"),
    url(r'^hosts_fangz/$', second_page_data, name="hosts_fangz"),
    url(r'^own_dialog/$', new_dialog, name="dialog"),
    url(r'^index_flash/$', index_flash, name="index_flash"),
]

urlpatterns += opreaters_urlparterns

from .union.role import list_all_users, add_user, delete_user, modify_user, sure_is_level0_user
role_urlparterns = [
    url(r'^list_all_users/$', list_all_users, name="list_all_users"),
    url(r'^add_user/$', add_user, name="add_user"),
    url(r'^delete_user/$', delete_user, name="delete_user"),
    url(r'^modify_user/$', modify_user, name="modify_user"),
    url(r'^sure_is_level0_user/$', sure_is_level0_user, name="sure_is_level0_user"),
]
urlpatterns += role_urlparterns


from .union.urls import urlpatterns as topo_urlpatterns
urlpatterns += topo_urlpatterns

from .aicruiser.urls import urlpatterns as aicruiser_urlparterns
urlpatterns += aicruiser_urlparterns