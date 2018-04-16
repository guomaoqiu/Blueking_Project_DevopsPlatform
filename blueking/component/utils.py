# -*- coding: utf-8 -*-
import json
import base64
import hmac
import hashlib


def get_signature(method, path, app_secret, params=None, data=None):
    """generate signature
    """
    kwargs = {}
    if params:
        kwargs.update(params)
    if data:
        data = json.dumps(data) if isinstance(data, dict) else data
        kwargs['data'] = data
    kwargs = '&'.join([
        '%s=%s' % (k, v)
        for k, v in sorted(kwargs.iteritems(), key=lambda x: x[0])
    ])
    orignal = '%s%s?%s' % (method, path, kwargs)
    signature = base64.b64encode(hmac.new(str(app_secret), orignal, hashlib.sha1).digest())
    return signature
