from django.conf.urls import url

from . import easy_view as views
from .is_active import have_logined
urlpatterns = [
    url(r'^login/$', views.log_in, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^logout/', views.log_out, name="logout"),
    url(r'^my_authenticate/$', views.my_authenticate, name="my_authenticate"),
    url(r'^have_logined/$', have_logined, name="have_logined"),
]