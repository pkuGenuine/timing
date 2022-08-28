from functools import wraps
from typing import Callable

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def identity_check(check_access: Callable = lambda x: True,
                   user_info_add: Callable = lambda x: x) -> Callable:
    """Perform user specific check,
    add generic user info, like name, avatar

    :param check_access: function to check access, defaults to lambdax:True
    :type check_access: Callable, optional
    :param user_info_add: , defaults to lambdax:x
    :type user_info_add: Callable, optional
    :return: _description_
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        @login_required()
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwds) -> HttpResponse | dict | None:
            assert check_access(request.user)
            ret = func(request, *args, **kwds)
            if isinstance(ret, tuple):
                template, frontend_dict = ret
                user_info_add(frontend_dict)
                return render(request, template, frontend_dict)
            # else, dict or None
            return ret
        return wrapper

    return decorator
