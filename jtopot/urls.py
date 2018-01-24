#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import url

from . import views
from .dj_views import *

urlpatterns = [
    ################# 0.2 版本前面的连接 #############
    url(r'^$', views.edit_index, name="edit_index"),
    url(r'^2$', views.edit2, name="edit2"),
    url(r'^show/$', views.show, name="show"),
    url(r'^get_canvas_size.config$', views.get_canvas_size, name="second_page"),
    url(r'^second_page_data/$', views.second_page_json, name="second_page_data"),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^second_page/$', views.second_page, name="second_page"),
    url(r'^get_json/$', views.get_json, name="get_json"),
    url(r'^add_json/$', views.add_json, name="add_json"),
    ################# 0.2#############
    url(r'^json1222/$', views.get_location_of_allnode, name="json1222"),

    ## 根据修改IP相关
    url(r'^add_ip/$', views.add_ip, name="add_ip"),
    url(r'^add_modal/$', views.add_modal, name="add_modal"),
    ##url(r'^edit_ip/$', views.edit_ip, name="add_ip"),
    url(r'^delete_ip/$', views.delete_ip, name="delete_ip"),
    url(r'^node_modal/$', views.get_get_modal, name="get_get_modal"),
    url(r'^canvas_size/$', views.canvas_size, name="canvas_size"),
    url(r'^test11/$', views.test_contatiner, name="test2222"),

    url(r'^svg.php$', views.new_topo, name="new_topo"),
    url(r'^q$', views.test1222, name="test1222"),

    url(r'^rand8/$', views.set_random_num8, name="set_random_num8"),
    url(r'^json_dj_nodes/$', json_dj_nodes, name="json_dj_nodes"),
    url(r'^dj_ip_dialog/$', dj_ip_dialog, name="dj_ip_dialog"),
]
