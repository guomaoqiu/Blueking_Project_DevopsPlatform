# -*- coding: utf-8 -*-
"""Django project settings
"""


try:
    from django.conf import settings

    APP_CODE = settings.APP_ID
    SECRET_KEY = settings.APP_TOKEN
    COMPONENT_SYSTEM_HOST = settings.BK_PAAS_HOST
except:
    APP_CODE = ''
    SECRET_KEY = ''
    COMPONENT_SYSTEM_HOST = ''

CLIENT_ENABLE_SIGNATURE = False
