from django.contrib import admin
from .models import *

admin.site.register(Incident)
admin.site.register(Followup)
admin.site.register(Notification)