# -*- coding: utf-8 -*-
"""
context_processor for common(setting)

除setting外的其他context_processor内容，均采用组件的方式(string)
"""
from django.conf import settings
import datetime


def mysetting(request):
    return {
        # 基础信息
        'RUN_MODE': settings.RUN_MODE,
        'APP_ID': settings.APP_ID,
        'SITE_URL': settings.SITE_URL,
        # 静态资源
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_VERSION': settings.STATIC_VERSION,
        # 登录跳转链接
        'LOGIN_URL': settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'BK_PAAS_HOST': '%s/app/list/' % settings.BK_PAAS_HOST,
        'BK_PLAT_HOST': settings.BK_PAAS_HOST,
        # 当前页面，主要为了login_required做跳转用
        'APP_PATH': request.get_full_path(),
        'NOW': datetime.datetime.now(),
        #'PRPCRYPTO_KEY':"2c70acf1-b78b-42c4-97a2"
    }
