# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsBkLogin(object):
    """Collections of bk_login APIS"""

    def __init__(self, client):
        self.client = client

        self.get_user = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/bk_login/get_user/',
            description=u'获取用户信息',
        )
