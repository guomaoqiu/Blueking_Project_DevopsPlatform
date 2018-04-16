# -*- coding: utf-8 -*-

from account.accounts import Account
from account.decorators import login_exempt


@login_exempt
def logout(request):
    account = Account()
    return account.logout(request)


@login_exempt
def check_failed(request):
    """权限验证错误页面"""
    account = Account()
    return account.check_failed(request)
