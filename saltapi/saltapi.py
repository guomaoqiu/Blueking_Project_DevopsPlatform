# -*- coding: utf-8 -*-
import json ,requests, sys, os
sys.path.append("./")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from settings import PRPCRYPTO_KEY
from home_application.models import ApiMg
from home_application.crypto import prpcrypt
import time
requests.packages.urllib3.disable_warnings()

class SaltApi(object):
    """docstring for SaltApi"""
    def __init__(self,app_name):
        '''
        @note 获取saltapi连接所需的账户密码及url
        @app_name代表saltapi所应用的场景，例如有两套satl环境时
        '''
        prpcrypt_key = prpcrypt(PRPCRYPTO_KEY)  # 调用crypto 解密
        app_env = ApiMg.objects.filter(app_name=app_name)
        for each_info in app_env:
            self.__user = each_info.to_json()["api_user"]
            # 连接密码
            self.__password = prpcrypt_key.decrypt(each_info.to_json()['api_paas'])
            # 连接url
            self.__salt_url = each_info.to_json()["api_url"]

            self.__token_id = self.get_saltapi_token(app_name)


    def get_saltapi_token(self,app_name):
        '''
        @note: 登录获取saltapi token
        @summary: 在登录之前查询数据库中的token是否过期(此处6个小时为有效期，配置文件中默认为12个小时)；如果过期则需登录获取，反之直接获取数据库中的
        '''
        salt = ApiMg.objects.all()

        old_token = salt[0].to_json()['api_token']
        old_token_createt = int(salt[0].to_json()['token_createt'])
        current_time = int(time.time())
        if (current_time - old_token_createt) > 43200 or old_token == '' : #Time (in seconds) for a newly generated token to live. Default: 12 hours
            #print '超过过期时间，需要更新token & 或 Token 此前为空'
            parmes={'eauth': 'pam' ,'username':self.__user,'password':self.__password}
            self.__salt_url += '/login'
            self.__my_headers = {
                'Accept': 'application/json'
            }
            try:
                req = requests.post(self.__salt_url, headers=self.__my_headers,data=parmes, verify=False,timeout=2)
                content = json.loads(req.content)
                token = content["return"][0]['token']
                p = ApiMg.objects.get(app_name=app_name)
                p.api_token = content["return"][0]['token']
                p.token_createt = int(time.time())
                p.save()
                return token
            except Exception,e:
                print e
            #return token
        else:
            print 'token还在有效期内直接从数据库获取'
            token = salt[0].to_json()['api_token']
            return token


    # run salt cmd
    def saltCmd(self, params):
        '''执行salt操作'''
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token':  self.__token_id
        }
        self.__salt_url = self.__salt_url.strip('/login')
        try:
            req = requests.post(self.__salt_url,data=params,headers=headers,verify=False,timeout=2)
            return req.content
        except Exception, e:
            print e

    def get_allhostname(self, params):
        '''执行salt操作'''
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token':  self.__token_id
        }
        self.__salt_url = self.__salt_url.strip('/login')

        try:
            req = requests.post(self.__salt_url,data=params,headers=headers,verify=False,timeout=2)

            return req.content
        except Exception, e:
            print e
            return e

    def all_key(self):
        '''
        @note: 获取所有的salt-key
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': self.__token_id
        }
        self.__salt_url = self.__salt_url.strip('/login')
        try:
            req = requests.post(self.__salt_url, data=params, headers=headers, verify=False,timeout=2)
            json_data = dict(json.loads(req.content)['return'][0])['data']['return']
            print json_data

            return json_data
        except Exception,e:
            print e


    def get_jid_result(self,jid):
        '''
        @note: 通过传入的jid获取结果
        '''
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': self.__token_id
        }
        self.__salt_url = self.__salt_url.strip('/login') + '/jobs/' + jid
        try:
            req = requests.get(self.__salt_url, headers=headers, verify=False,timeout=2)
            json_data = req.content
            
            return json_data
        except Exception,e:
            print e

    def get_minions(self, host):
        '''
    	@note: 收集主机minion信息
    	'''
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': self.__token_id
        }
        url = self.__salt_url.strip('/login') + ('/minions/%s' % host)

        req = requests.get(url, headers=headers, verify=False,timeout=2)
        json_data = json.loads(req.content)


        hostname = host.encode('raw_unicode_escape')
        release = json_data['return'][0]["%s" % host]["osfullname"].encode('raw_unicode_escape') + ' ' + json_data['return'][0]["%s" % host]["osrelease"].encode('raw_unicode_escape')
        kernelrelease = json_data['return'][0]["%s" % host]["kernelrelease"].encode('raw_unicode_escape')
        num_cpus = json_data['return'][0]["%s" % host]["num_cpus"]
        cpu_type= json_data['return'][0]["%s" % host]["cpu_model"].encode('raw_unicode_escape')
        mem_total = json_data['return'][0]["%s" % host]["mem_total"]
        private_ip = json_data['return'][0]["%s" % host]["ip4_interfaces"]["eth0"][0].encode('raw_unicode_escape')
        info = {
            'hostname': hostname,
            'os_release': release,
            'mem_total': mem_total,
            'num_cpus': num_cpus,
            'cpu_type':cpu_type,
            'private_ip': private_ip,
            'public_ip': '',
            'kernelrelease': kernelrelease
        }
        return info
