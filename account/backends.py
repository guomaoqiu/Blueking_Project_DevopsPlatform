# -*- coding: utf-8 -*-
"""自定义认证类."""

from django.contrib.auth.backends import ModelBackend

from account.accounts import Account


class BkBackend(ModelBackend):
    """自定义认证方法."""

    def authenticate(self, request):
        account = Account()
        login_status, user = account.is_bk_token_valid(request)
        if not login_status:
            return None
        return user
