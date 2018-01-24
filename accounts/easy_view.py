from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import WebUser, ProjUser


def log_in(request):
    return render(request, "easy_auth/login.html", {})


## 创建小喽喽角色
def register(request):
    username= request.GET["username"]
    password = request.GET["password"]
    WebUser.objects.get_or_create(username=username, password=password)
    ProjUser.objects.get_or_create(username=username, password=password, email=str(username)+"@qldl.com")

    return HttpResponse("注册账号成功")


def log_out(request):
    try:
        logout(request)
    except:
        pass
    return redirect('/')


def my_authenticate(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if username in [data.username for data in list(WebUser.objects.all())]:
        temp_user = WebUser.objects.get(username=username)
        if temp_user.password == password:
            user = ProjUser.objects.get(username=username)
            login(request, user)
            return HttpResponse("登陆成功")

        return HttpResponse("密码不正确")
    return HttpResponse("用户名不存在")
