# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsMY_APP(object):
    """Collections of my_app APIS"""

    def __init__(self, client):
        self.client = client

        self.get_flask_content = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/my_app/get_flask_content/',
            description=u'调用Flask_Api_Content',
        )


