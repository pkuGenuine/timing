from functools import wraps
from typing import Callable, Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.utils import add_user_info


def identity_check(
        template: str = "",
        check_access: Optional[Callable] = None
    ) -> Callable:
    """Perform user specific check.
    If template is not '', render with some of user info,
        like name, avatar, etc.

    :param template: html template file name, like 'base.html'
    :type check_access: str
    :param check_access: function to check access
    :type check_access: Callable, optional
    :return: actual decorator
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        @login_required()
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwds) -> HttpResponse | dict | None:
            if check_access:
                check_access(request.user)
            ret = func(request, *args, **kwds)
            if template:
                add_user_info(request.user, ret)
                return render(request, template, ret)
            return ret
        return wrapper

    return decorator
