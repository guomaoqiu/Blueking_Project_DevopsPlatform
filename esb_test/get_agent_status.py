# -*- coding: utf-8 -*-
import json,requests
def get_agent_status():
    '''
    @note: 通过http协议来调用获取agent的状态
    '''
    # 组件地址
    api_url='http://paas.sctux.com:80/api/c/compapi/job/get_agent_status/'
    # 传递参数
    parmas = {
        # 应用信息中的APP_ID
        'app_code': 'demoapp',
        # 应用信息中的APP_TOKEN
        'app_secret': '2c70acf1-b78b-42c4-97a2-cfcfe7c58347',
        # 由于这里单独写的脚本来测试，所以直接使用F12查看得到，
        # 如果是蓝鲸体系中调用的这里改为 `request.COOKIES['bk_token']` 即可
        'bk_token': 'JPiEWCxyUYG53z0id-S-zsDTz8mnFJ3juahtceCVfuM',
        # 业务ID
        'app_id': 2,
        # IP信息，每项条目包含信息见下面参数描述
        'ip_infos': [
                {
                    "ip": "192.168.56.128",
                    # 该IP的子网ID 已经提前抓取到了
                    "plat_id": 1,
            }
        ]
    }
    res = requests.post(url=api_url, data=json.dumps(parmas))
    print json.dumps(res.json(),indent=2, ensure_ascii=False)

if __name__ == "__main__":
    get_agent_status()


# 通过job工作台查看执行结果
# run: python test1.py