from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


class ProjUser(AbstractUser):
    # nickname = models.CharField('昵称', max_length=50, blank=True)
    mugshot = models.ImageField('头像', upload_to='uploads/mugshots', default="mugshots/logo400x400.jpg")
    role = models.CharField('身份', max_length=50, default="网络管理员")

    # objects = BlogUserManager()

    def get_absolute_url(self):
        return "/u/{}/".format(self.id)

    def __str__(self):
        return self.username

    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        return url

    class Meta:
        verbose_name = "网站扩展用户"


class WebUser(models.Model):
    ### 安全主管, 网络管理员, 超级管理员(new—用户)
    username = models.CharField('用户名', max_length=50)
    password = models.CharField('密码', max_length=50)
    role = models.CharField('角色', max_length=50, default="网络管理员")

    def __str__(self):
        return self.role + ": " + self.username

    class Meta:
        verbose_name = "用户验证"









