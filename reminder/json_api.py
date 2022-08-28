from datetime import datetime

from django.http import HttpRequest

from general_utils.decorator import generic_checker
from account.decorator import identity_check
from reminder.models import DailyTask, DailyTaskRecord


@generic_checker(accept_method_list=['POST'], ret_json=True)
@identity_check()
def daily_task(request: HttpRequest, title: str) -> dict | None:
    """API to manipulate daily task object
    Not take concurrency into consideration

    :param request: 
    :type request: HttpRequest
    :param title: 
    :type title: str 
    :return: 
    :rtype: dict | None
    """
    # REMARK: `get_or_creat` require uniqueness to become atomic
    # https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
    task = DailyTask.objects.get_or_create(title=title,
                                           user=request.user)
    operation = request.POST['operation']
    if operation == 'create':
        return
    if operation == 'update':
        ...
    if operation == 'delete':
        ...
    raise ValueError(f'Unsupported opr: {operation}')


@generic_checker(accept_method_list=['POST'], ret_json=True)
@identity_check()
def daily_record(request: HttpRequest, title: str):
    """API to manipulate TODAY'S daily task record object
    Not take concurrency into consideration

    :param request: 
    :type request: HttpRequest
    :param title: 
    :type title: str
    """
    today = datetime.now().date()
    task = DailyTask.objects.get(title=title,
                                 user=request.user,
                                 active=True)
    operation = request.POST['operation']
    if operation in ['check', 'update']:
        record, _ = DailyTaskRecord.objects.get_or_create(
            date=today,
            task=task,
        )
        remark = request.POST['remark']
        if remark:
            DailyTaskRecord.objects.filter(
                id=record.id
            ).update(remark=remark)
    elif operation == 'uncheck':
        DailyTaskRecord.objects.filter(
            date=today,
            task=task,
        ).update(status=DailyTaskRecord.RecordStatus.UNCHECK)
    raise ValueError(f'Unsupported opr: {operation}')
