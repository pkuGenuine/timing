import os
from functools import wraps
from typing import Callable, List
import logging

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from general_utils.log import log_exception


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
fh = logging.FileHandler(os.path.join(settings.LOG_ROOT, 'exception.log'))
fh.setLevel(settings.LOG_LEVEL)
logger.addHandler(fh)


def generic_checker(accept_method_list: List[str] = ['GET', 'POST'],
                    ret_json=False) -> Callable:
    """Perform user-independent check, 
    capture any unexpected exception, and profiling

    If ret_json is true, wrapped_response can return None, the decorator
        will return a dict('valid=False').

    :param accept_method_list: http request methods, defaults to ['GET', 'POST']
    :type accept_method_list: List[str], optional
    :param ret_json: return json or not (http), defaults to False
    :type ret_json: bool, optional
    :return: decorator
    :rtype: Callable
    """
    def decorator(wrapped_response: Callable) -> Callable:
        @wraps(wrapped_response)
        def wrapper(request: HttpRequest, *args, **kwds):
            try:
                assert request.method in accept_method_list, \
                    f'HTTP {request.method} request not supported. Want {accept_method_list}'
                ret = wrapped_response(request, *args, **kwds)
                if ret_json:
                    ret.update(valid=True)
                    return JsonResponse(ret)
                return ret 
            except Exception as e:
                if settings.DEBUG:
                    raise
                log_exception(logger, e)
                if ret_json:
                    return JsonResponse(dict(valid=False))
                return redirect('/error_page')
        return wrapper
    return decorator
