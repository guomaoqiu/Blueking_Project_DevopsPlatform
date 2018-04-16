# -*- coding: utf-8 -*-
import logging

from .client import ComponentClient
from . import conf

logger = logging.getLogger('component')

__all__ = [
    'get_client_by_request',
    'get_client_by_user',
]


def get_client_by_request(request, **kwargs):
    """根据当前请求返回一个client

    :param request: 一个django request实例
    :returns: 一个初始化好的ComponentClint对象
    """

    if request.user.is_authenticated():
        bk_token = request.COOKIES.get('bk_token', '')
    else:
        bk_token = ''

    common_args = {
        'bk_token': bk_token,
    }
    common_args.update(kwargs)
    return ComponentClient(conf.APP_CODE, conf.SECRET_KEY, common_args=common_args)


def get_client_by_user(user, **kwargs):
    """根据user实例返回一个client

    :param user: User实例或者User.username数据
    :returns: 一个初始化好的ComponentClint对象
    """
    try:
        from account.models import BkUser as User
    except:
        from django.contrib.auth.models import User

    try:
        if isinstance(user, User):
            username = user.username
        else:
            username = user
    except:
        logger.exception(u'根据user（%s）获取用户失败' % user)

    common_args = {'username': username}
    common_args.update(kwargs)
    return ComponentClient(conf.APP_CODE, conf.SECRET_KEY, common_args=common_args)
