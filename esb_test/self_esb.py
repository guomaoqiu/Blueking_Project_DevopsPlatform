# -*- coding: utf-8 -*-
'''
自主式接入esb，需要在ESB页面上配置填写相关信息
# 这里使用的是第三方接口(Flask随便跑的一个例子)
'''
import json,requests
def run_self_esb():

    api_url="http://paas.sctux.com:80/api/c/self-service-api/myapp/esb_test/"
    data = {
        'app_code': "demoapp",
        'app_secret': "2c70acf1-b78b-42c4-97a2-cfcfe7c58347",
        'bk_token': '5geUPjvUAoMJyJJae11DrFOp4NpKs7VNDBykpf37H_k',
    }
    res = requests.get(url=api_url, params=data)
    print json.dumps(res.json(),indent=2, ensure_ascii=False)

if __name__ == "__main__":
    run_self_esb()

#run: python self_esb.py