from django.contrib import admin
from reminder.models import DailyTask, DailyTaskRecord

@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'active']


@admin.register(DailyTaskRecord)
class DailyTaskRecordAdmin(admin.ModelAdmin):
    list_display = ['task', 'date']