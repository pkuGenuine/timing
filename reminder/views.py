from django.http import HttpRequest

from general_utils.decorator import generic_checker
from account.decorator import identity_check
from reminder.models import DailyTask


@generic_checker()
@identity_check(template='daily_check.html')
def daily_check(request: HttpRequest) -> dict:
    """daily task check page
    """
    active_tasks = DailyTask.objects.filter(user=request.user,
                                            active=True)
    frontend_dict = dict(active_tasks=active_tasks)
    return frontend_dict


@generic_checker()
@identity_check(template='daily_check_management.html')
def daily_manage(request: HttpRequest) -> dict:
    """daily task manage page
    """
    all_tasks = DailyTask.objects.filter(user=request.user)
    frontend_dict = dict(all_tasks=all_tasks)
    return frontend_dict


@generic_checker()
@identity_check(template='daily_check_display.html')
def daily_display(request: HttpRequest) -> dict:
    """daily task summary display page
    """
    active_tasks = DailyTask.objects.filter(user=request.user,
                                            active=True)
    frontend_dict = dict(active_tasks=active_tasks)
    return frontend_dict


@generic_checker()
@identity_check(template='weekly_report.html')
def weekly_report(request: HttpRequest) -> dict:
    frontend_dict = {}
    return frontend_dict
