from functools import wraps
from typing import Callable, List

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.shortcuts import render


class RenderWithIdentity():

    def __init__(self, required_method_list: List[str] = ['GET', 'POST']):
        self.method_checker = require_http_methods(required_method_list)

    def __call__(self, func: Callable) -> Callable:

        @login_required()
        @self.method_checker
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwds) -> HttpResponse:
            template, frontend_dict = func(request, *args, **kwds)
            return render(request, template, frontend_dict)
        return wrapper


class IdentityCheck():

    def __init__(self, required_method_list: List[str] = ['GET', 'POST']):
        self.method_checker = require_http_methods(required_method_list)

    def __call__(self, func: Callable) -> Callable:

        @login_required()
        @self.method_checker
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwds) -> HttpResponse:
            return func(request, *args, **kwds)
        return wrapper
