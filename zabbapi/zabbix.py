#!~/zero/bin/python /data/study/flask-login-register2/app/scripts/zabbix_delete.py
#-*- coding:utf8 -*-
# 在3.0版本d中host.exists方法已经去除，所以这里判断主机是否存在的方式是获取所有主机的hostname
# 再进行判断.
import xlrd, os
from pyzabbix import ZabbixAPI
import json ,requests, sys, os
sys.path.append("./")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from settings import PRPCRYPTO_KEY
from home_application.models import ApiMg
from home_application.crypto import prpcrypt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ZabbixAction(object):
#########################
#    Global   Features  #
#########################
    i=0

    host_name_list = []
    host_id_list = []

    file_name = file


#### init
    def __init__(self,app_name):
        prpcrypt_key = prpcrypt(PRPCRYPTO_KEY)  # 调用crypto 解密
        app_env = ApiMg.objects.filter(app_name=app_name)
        for each_info in app_env:
            self.__user = each_info.to_json()["api_user"]
            # 连接密码
            self.__password = prpcrypt_key.decrypt(each_info.to_json()['api_paas'])
            # 连接url
            self.__url = each_info.to_json()["api_url"]

#### 登录zabbix
    def login(self):
        try:
            self.zapi = ZabbixAPI(self.__url)
            self.zapi.login(self.__user,self.__password)
            #fo.write("【登录ZabbixApi接口成功】\n ")
            print "【登录ZabbixApi接口成功】\n "
        except:
            #fo.write("【登录ZabbixApi接口成功】\n ")
            print "\n【登录zabbix平台出现错误】"
            #sys.exit()

#### 获取现zabbix中的所有主机 __get_host:私有属性
    def get_host(self):
        for i in self.zapi.host.get():
            #print i
            self.host_name_list.append(str(i['name']))
            self.host_id_list.append(str(i['hostid']))
        all_host = dict(zip(self.host_name_list, self.host_id_list))
        return all_host

#########################
#    ZabbixAdd   Host   #
#########################
#### 通过模板名获取模板ID
    def get_templateid(self,template_name):
        template_data = {
            "host": [template_name]
        }
        result = self.zapi.template.get(filter=template_data)
        if result:
            return result[0]['templateid']
        else:
            return result
#### 通过组名获取组ID
    def get_groupid(self, group_name):
        group_data = {
            "name": [group_name]
        }
        return str(self.zapi.hostgroup.get(filter=group_data)[0]['groupid'])

#### 打开xls文件
    def open_excel(self, file=file_name):
      try:
          data = xlrd.open_workbook(file)
          return data
      except Exception, e:
          print str(e)


#### 将xls文件内主机导入到list
    def create_hosts(self, file):
        self.get_host()
        data = self.open_excel(file)
        # print data.sheets()[0]
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        list = []
        for rownum in range(1, nrows):
            list.append(table.row_values(rownum))
        fo = open('/tmp/cache_add_zabbix.txt', 'w')
        for host in list:
            host_name = host[0]
            visible_name = host[1]
            host_ip = host[2]
            group = host[3]
            groupid = self.get_groupid(group)
            template = host[4]
            templateid = self.get_templateid(host[4])
            inventory_location = host[5]

            host_data = {
                "host": host_name,
                "name": visible_name,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": host_ip.strip(),
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                  {
                      "groupid": groupid
                  }
              ],
                "templates": [
                  {
                      "templateid": templateid
                  }
              ],
                 "inventory": {
                  "location": inventory_location
              }
            }

          # Create Host
            if host_data['name'] in self.host_name_list:
                s1 = ("<U+274C> 主机: %s 已存在 请核实.!") % str(host_data["name"])
                fo.write(s1)
            else:
                self.zapi.host.create(host_data)
                s2 = ("✔️ 添加主机: %s 成功.!") % str(host_data["name"])
                fo.write(s2)
        fo.close()


#########################
#    ZabbixDelete  Host #
#########################

#### 删除主机
    def delete_host(self,server_list):
      fo = open('/tmp/cache_delete_zabbix.txt','w')
      res = []
      id = []

      [ res.append(i.replace(' ','')) for i in server_list ]
      #print res

      for host_name in res:
          #print host_name
          if host_name not in self.get_host().keys():
              s1 = ("<U+274C> 主机 %s 不存在或已删除,请核实.!") % str(host_name)
              print ("<U+274C> 主机 %s 不存在或已删除,请核实.!") % str(host_name)
              fo.write(s1)
              #return  u"\033[1;31m 主机 %s 不存在或已删除,请核实！\033[0m" % host_name
          else:
              data = {"name":[host_name]}
              for host_id  in str(self.zapi.host.get(filter=data)[0]['hostid']).split('\n'):
                  s2 = ("✔️ 主机:  %s ID: %s 删除成功.!") % (str(host_name),str(host_id))
                  print ("✔️ 主机:  %s ID: %s 删除成功.!") % (str(host_name),str(host_id))
                  fo.write(s2)
                  #return u"\033[1;32m 主机:  %s   ID: %s 删除成功！\033[0m" % (host_name,host_id)
                  id.append(host_id)
                  self.zapi.host.delete(host_id)
      fo.close()

#########################
#    GetZabbix  Data    #
#########################

#### 获取特别指定主机的id，通过传入主机名
    def get_each_host(self,hostname):
        data = {
            "output": "extend",
            "filter" : {"name": hostname}
        }
        print hostname
        for i in self.zapi.host.get(**data):
            return i['hostid']

#### 获取特定主机的组名称
    def get_each_groupname(self, hostname):
        data = {
            "output": "extend",
            "filter": {"name": hostname}
        }
        #print hostname
        res =  self.zapi.host.get(**data)

        print res

#### 获取指定主机的graph_name对应的graph_id
    def get_graph(self, hostid, graph_name):
        data = {
            "output": "extend",
            "hostids": hostid,
            "sortfield": "name",
            "search": graph_name
        }
        print graph_name
        ret = self.zapi.graph.get(**data)
        return ret

##### 通过组id获取相关组内的所有主机
    def get_hostingroup(self,groupids):
        data = {
        "output": ["groupid",'name'],
        "groupids": groupids
        }
        host_list=[]
        ret = self.zapi.host.get(**data)
        for i in ret:
            host_list.append(i['name'])
        return  host_list
#
#### 通过特定主机名获取主机对应的主机组
    def get_host_groupname(self,hostname):
        data = {
            "output": ['groupid','name'],
            "filter": "name"
        }
        group_id=[]
        group_name=[]

        for i in self.zapi.hostgroup.get(**data):
            group_name.append(str(i['name']))
            group_id.append(str(i['groupid']))
        res = dict(zip(group_name,group_id))
        for k,v in res.items():
            for host_name in self.get_hostingroup(v):
                if host_name == hostname:
                    return k
###
client = ZabbixAction("zabbix")
client.login()
print client.get_host()
