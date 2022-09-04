from django.urls import path

from reminder import views, json_api

urlpatterns = [
    ### daily task releated
    path('daily_check', views.daily_check, name='daily_check'),
    path('daily_manage', views.daily_manage, name='daily_manage'),
    path('daily_display', views.daily_display, name='daily_display'),
    # reverse('daily_task', kwargs={'title':'ttt'})
    path('daily_task/<str:title>', json_api.daily_task, name='daily_task'),
    path('daily_record/<str:title>', json_api.daily_record, name='daily_record'),
    ### weekly report related
    path('weekly_report', views.weekly_report, name='weekly_report')
]