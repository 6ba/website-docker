

def cunzhen(request):
    ## 外发次数最多的IP
    sql = """select src_ip, COUNT(src_ip) from user_alert group by src_ip;"""


    pass