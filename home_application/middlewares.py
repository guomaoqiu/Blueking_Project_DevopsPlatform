# -*- coding: utf-8 -*-
from django.conf import settings
import requests,json
from common.mymako import render_mako_context
from account.accounts import Account
from django.http.response import HttpResponseRedirect


class CheckAccessMiddleware(object):
    '''
    @note: app权限检查中间件
    '''
    def process_request(self, request):
        account = Account() # 通过登录态获取用户名
        username =  account.is_bk_token_valid(request)[1]

        # 获取登录主页后生成的 session
        is_login = request.session.get('logined',None)

        # 如果session & username不存在则直接去请求权限app
        if is_login is None and username is not None:

            url = settings.BK_PAAS_HOST + "/o/bkpermission/" + "return_result_b/?app_code=" + settings.APP_ID  + "&username=" + str(username)
            redirect_url =  settings.BK_PAAS_HOST + "/o/bkpermission" + '/return_forbidden/' + "?username=" + str(username)

            print url
            res = json.loads(requests.get(url=url).content)
            if not res['result']:
               '''
               @note: 重定向到403页面
               '''
               return HttpResponseRedirect(redirect_url)
