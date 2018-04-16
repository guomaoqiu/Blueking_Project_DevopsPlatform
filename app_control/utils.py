# -*- coding: utf-8 -*-

from app_control.models import Function_controller


def func_check(func_code):
    """
    @summary: 检查功能是否开放
    @param func_code: 功能ID
    @return (1/2/3, message)
            #如下 (0, 功能未开启)
                  (1, 功能已开启)
    """
    result, enabled = Function_controller.objects.func_check(func_code)
    return (enabled, u"功能已开启" if enabled else u"功能未开启")
