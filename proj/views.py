from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth.views import login_required

@login_required
def index(request):
    return render(request, "proj/index.html", {})

def homepage(request):
    return render(request, "proj/index.html", {})

def intercept(request):
    return render(request, "proj/pages/intercept.html", )

def logs(request):
    return render(request, "proj/pages/logs.html", )

def monitor(request):
    return render(request, "proj/pages/monitor.html", )

def m(request):
    return render(request, "proj/pages/m.html", )

def risk_d(request):
    return render(request, "proj/pages/risk_d.html", )

def warn_risk(request):
    return render(request, "proj/pages/warn_risk.html", )

def risk_d_s(request):
    request.session["task_id"] = request.GET["task_id"]
    return render(request, "proj/pages/risk_d_s.html", )

def scanning(request):
    return render(request, "proj/pages/scanning.html", )

def setting(request):
    return render(request, "proj/pages/setting.html", )

def setting1(request):
    return render(request, "proj/pages/setting1.html", )

def setting2(request):
    return render(request, "proj/pages/setting2.html", )

def setting3(request):
    return render(request, "proj/pages/setting3.html", )

def souquan(request):
    return render(request, "proj/pages/souquan.html", )

def task_d(request):
    return render(request, "proj/pages/task_d.html", )

def voucher(request):
    return render(request, "proj/pages/voucher.html", )

def voucher_all(request):
    return render(request, "proj/pages/voucher_all.html", )

def voucher_in(request):
    return render(request, "proj/pages/voucher_in.html", )

def voucher_out(request):
    return render(request, "proj/pages/voucher_out.html", )

def warning(request):
    return render(request, "proj/pages/warning.html", )

def warningdetail(request):
    request.session["eid"] = request.GET["id"]
    return render(request, "proj/pages/warningdetail.html", )


from django.shortcuts import redirect
def favicon(request):
    return redirect("/static/media/favicon.ico")


