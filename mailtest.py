# -*- coding:utf-8 -*-

'''
调用 通知组件邮件发送样例
'''
import requests
import simplejson as json

url = "http://paas.moefantasy.org:88/api/c/compapi/cmsi/send_mail/"

headers = {'Content-type': 'application/json'}

data = {
    'app_code': 'bk_monitor',
    'app_secret': 'd9524bb7-23ab-4e9c-bf55-f4e8cce2c499',
    'username': 'admin',
    'receiver__username': 'admin',
    'content': 'content',
    'title': 'test',
    'sender':'郭茂秋',
    'is_content_base64': True
}

req = requests.post(url, data=json.dumps(data),headers=headers)

print req.text