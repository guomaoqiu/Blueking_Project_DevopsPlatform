# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from common.log import logger


def error_404(request):
    """
    404提示页
    """
    return render_mako_context(request, '404.html')


def error_500(request):
    """
    500提示页
    """
    return render_mako_context(request, '500.html')


def error_401(request):
    """
    401提示页
    """
    return render_mako_context(request, '401.html')


def error_403(request):
    """
    403提示页
    """
    return render_mako_context(request, '403.html')
