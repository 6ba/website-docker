from django.http import HttpResponse
### 判断用户是不是登陆状态

def have_logined(request):
    if request.user.is_authenticate():
        return HttpResponse(0)
    else:
        return HttpResponse(1)