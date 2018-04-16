# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
# from django.contrib import admin
# from apps.__.models import aaaa
#
# admin.site.register(aaaa)
# ===============================================================================
from django.contrib import admin
from djcelery.models import TaskMeta


class TaskMetaAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'status', 'result', 'date_done', 'traceback')


admin.site.register(TaskMeta, TaskMetaAdmin)

