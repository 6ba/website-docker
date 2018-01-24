from django.contrib import admin

# Register your models here.
"""
select t1.event_stat, user_alert.src_ip as gj_ip, self_cruiser.src_ip as zjip from (select * from proj_eventdetail) as t1 
                   left join 
                    user_alert 
                   on t1.event_id = user_alert.id
                   left join 
                   self_cruiser 
                   on t1.event_id = self_cruiser.id;

"""