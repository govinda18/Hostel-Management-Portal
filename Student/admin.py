# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Hostel)
admin.site.register(Notifcation)
admin.site.register(HostelProfile)
admin.site.register(Profile)
admin.site.register(GrievanceCategory)
admin.site.register(Grievance)
admin.site.register(Branch)
admin.site.register(HostelAllotment)
admin.site.register(Roominfo)