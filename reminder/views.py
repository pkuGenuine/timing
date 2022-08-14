from typing import Tuple
from django.http import HttpRequest

from general_utils.decorator import HtmlViewResponse
from account.decorator import RenderWithIdentity
from reminder.models import DailyTask


RenderParam = Tuple[str, dict]


@HtmlViewResponse()
@RenderWithIdentity()
def daily_check(request: HttpRequest) -> RenderParam:
    """daily task check page
    """
    active_tasks = DailyTask.objects.filter(user=request.user,
                                            active=True)
    frontend_dict = dict(active_tasks=active_tasks)
    return 'daily_check.html', frontend_dict


@HtmlViewResponse()
@RenderWithIdentity()
def daily_manage(request: HttpRequest) -> RenderParam:
    """daily task manage page
    """
    all_tasks = DailyTask.objects.filter(user=request.user)
    frontend_dict = dict(all_tasks=all_tasks)
    return 'daily_check_management.html', frontend_dict


@HtmlViewResponse()
@RenderWithIdentity()
def daily_display(request: HttpRequest) -> RenderParam:
    """daily task summary display page
    """
    active_tasks = DailyTask.objects.filter(user=request.user,
                                            active=True)
    frontend_dict = dict(active_tasks=active_tasks)
    return 'daily_check_display.html', frontend_dict
