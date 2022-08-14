from functools import wraps
from typing import Callable

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect


class SimpolJsonResponse():

    def __init__(self):
        ...

    def __call__(self, func: Callable) -> Callable:
        """Capture exception and return valid: False

        Otherwise, return valid: True

        :param func: 
        :type func: Callable
        :return: 
        :rtype: Callable
        """

        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwds):
            try:
                response = dict(valid=True)
                ret = func(request, *args, **kwds)
                if ret is not None:
                    response.update(**ret)
                return JsonResponse(response)
            except:
                # TODO: if debug, raise
                return JsonResponse(dict(valid=False))
        return wrapper


class HtmlViewResponse():

    def __init__(self):
        ...

    def __call__(self, wrapped_view: Callable) -> Callable:
        """Capture exception and redirect error page

        :param wrapped_view: 
        :type wrapped_view: Callable
        :return: 
        :rtype: Callable
        """

        @wraps(wrapped_view)
        def wrapper(request: HttpRequest, *args, **kwds):
            try:
                return wrapped_view(request, *args, **kwds)
            except Exception as e:
                # TODO: log it
                return redirect('/error_page')
        return wrapper

