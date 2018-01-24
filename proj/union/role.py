"""创建用户中心; 角色机制"""
from django.http import JsonResponse, HttpResponse

from accounts.models import WebUser, ProjUser
from datetime import datetime, timedelta

def add_user(request):
    if request.method == "POST":
        data = request.POST
        password = data["password"]
        role = data["role"]
        username = data["username"]

        webuser_params = {
            "username": username,
            "password": password,
            "role": role
        }

        proj_user_params = {
            "username": username,
            "password": password,
            "email": username + "@actanble.com",
            "last_login": datetime.now(),
            "date_joined": datetime.now() - timedelta(days=7),
            "role": role
        }
        ProjUser.objects.get_or_create(**proj_user_params)
        WebUser.objects.get_or_create(**webuser_params)
        return HttpResponse("创建成功！")


def list_all_users(request):
    all_users = ProjUser.objects.all()
    res_user_records = []
    res_user_lists = []
    for user in all_users:
        params = {
            "username": user.username,
            "last_login": str(user.last_login),
            "date_joined": str(user.date_joined),
            "role": user.role,
            "user_id": user.id
        }

        if user.is_superuser:
            user_record_str = """{username},超级管理员,{date_joined},{last_login}""".format(**params)
            temp_str = """{username},超级管理员,""".format(**params)
        else:
            temp_str = """{username},{role},
            <td><i class='fa fa-eyedropper ifir' onclick="modify_user({user_id})"></i>
            <i class='fa fa-remove isec' style='margin-left:20px;' onclick="delete_user({user_id})"></i></td>
            """.format(**params)
            user_record_str = """{username},{role},{date_joined},{last_login}""".format(**params)

        res_user_lists.append(temp_str.split(","))
        res_user_records.append(user_record_str.split(","))

    return JsonResponse({"res_user_lists": res_user_lists, "res_user_records":res_user_records})


def delete_user(request):
    user_id = int(request.GET["user_id"])
    user = ProjUser.objects.get(id=user_id)
    temp_username = user.username
    user.delete()
    webuser = WebUser.objects.get(username=temp_username)
    webuser.delete()
    return HttpResponse("删除角色"+ temp_username + "成功！")


def modify_user(request):
    if request.method == "GET":
        user_id = int(request.GET["user_id"])
        user = ProjUser.objects.get(id=user_id)
        return JsonResponse({
            "username": user.username,
            "password": "112233..",
            "role": user.role
        })


def sure_is_level0_user(request):
    if request.user.role == "网络管理员":
        return HttpResponse(0)
    return HttpResponse(1)





