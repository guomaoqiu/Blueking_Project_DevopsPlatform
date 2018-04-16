# -*- coding: utf-8 -*-
"""Login middleware."""

from django.contrib.auth import authenticate
from django.middleware.csrf import get_token as get_csrf_token
from common.mymako import render_mako_context
from account.accounts import Account
from django.conf import settings
import json,requests

class LoginMiddleware(object):
    """Login middleware."""

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        if getattr(view, 'login_exempt', False):
            return None
        user = authenticate(request=request)
        if user:
            request.user = user
            get_csrf_token(request)
            return None

        account = Account()
        return account.redirect_login(request)
