from django.contrib import admin

# Register your models here.
from .models import ProjUser, WebUser

admin.site.register(ProjUser)
admin.site.register(WebUser)
"""

          <section class="col-lg-8 connectedSortable topout">
              {% include 'proj/pages/own_add/jtopo.html' %}
             {% include 'proj/pages/own_add/modal.html' %}
          </section><!-- /.Left col -->
"""

