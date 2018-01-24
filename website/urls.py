from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from proj.views import index, favicon
from django.contrib import admin

urlpatterns = [
      url(r'^superadmin/', admin.site.urls),
      # url(r'^favicon.ico$', favicon),
      url(r'', include('accounts.easy_urls', namespace='account', app_name='accounts')),
      url(r'^$', index, name="项目主页"),
      url(r'jtopo/', include('jtopot.urls', namespace='jtopot', app_name='jtopot')),
      url(r'proj/', include('proj.urls', namespace='proj', app_name='proj')),

  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
