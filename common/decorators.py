# -*- coding: utf-8 -*-

"""
@summary: 装饰器
@usage：
          >>> from common.decorators import escape_exempt, escape_script, escape_url
          >>> @escape_exempt()
          >>> @escape_script()
          >>> @escape_url()
          >>> def test_func(request):
          >>>     pass
"""

from django.utils.decorators import available_attrs
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


# ===============================================================================
# 转义装饰器
# ===============================================================================
def escape_exempt(view_func):
    """
    转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_texteditor(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数作为富文本编辑内容处理
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_script = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_url(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行url escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_url = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
