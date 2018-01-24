from django.conf.urls import url

from .dj_views import *

urlpatterns = [
    url(r'^add_ip_to_topoarea/$', add_ip, name="add_ip_to_topoarea"),
    url(r'^delete_ip_from_topoarea/$', delete_ip, name="delete_ip_from_topoarea"),


    url(r'^dj_topo_dialog/$', dj_topo_dialog, name="dj_topo_dialog"),

]