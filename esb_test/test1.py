# -*- coding: utf-8 -*-
'''
直接通过http协议来调用
'''
import json,requests

def excute_task():
    api_url='http://paas.sctux.com:80/api/c/compapi/job/execute_task/'
    parmas = {
        # 应用信息中的APP_ID
        'app_code': 'demoapp',
        # 应用信息中的APP_TOKEN
        'app_secret': '2c70acf1-b78b-42c4-97a2-cfcfe7c58347',
        # 由于这里单独写的脚本来测试，所以直接使用F12查看得到，
        # 如果是蓝鲸体系中调用的这里改为 `request.COOKIES['bk_token']` 即可
        'bk_token': '5geUPjvUAoMJyJJae11DrFOp4NpKs7VNDBykpf37H_k',
        # 作业ID
        'task_id': 1,
        # 业务ID
        'app_id': 2,
    }
    res = requests.post(url=api_url, data=json.dumps(parmas))
    print json.dumps(res.json(),indent=2, ensure_ascii=False)

if __name__ == "__main__":
    excute_task()

# 通过job工作台查看执行结果
# run: python test1.py