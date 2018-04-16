# -*- coding: utf-8 -*-
from django.db import models
import datetime
from crypto import prpcrypt
from settings import PRPCRYPTO_KEY

class Hostinfo(models.Model):

    hostname = models.CharField(u"主机名",max_length=30)
    public_ip = models.CharField(u"公网IP",max_length=30)
    private_ip = models.CharField(u"内网IP",max_length=30)
    mem_total = models.CharField(u"总内存",max_length=30)
    cpu_type = models.CharField(u"CPU类型",max_length=120)
    num_cpus = models.CharField(u"CPU颗数",max_length=30)
    os_release = models.CharField(u"系统版本",max_length=30)
    kernelrelease = models.CharField(u"内核版本",max_length=120)

    def to_json(self):
        return {
        		'id':self.id,
                'hostname' : self.hostname,
                'public_ip' : self.public_ip,
                'private_ip' : self.private_ip,
                'mem_total' : self.mem_total,
                'cpu_type'  : self.cpu_type,
                'num_cpus' : self.num_cpus,
                'os_release': self.os_release,
                'kernelrelease': self.kernelrelease
        }

# api 管理
class ApiMg(models.Model):
    app_name =  models.CharField(max_length=30)
    api_user = models.CharField(max_length=30,null=False)
    api_paas = models.CharField(max_length=80,null=False)
    api_token = models.CharField(max_length=80,null=True)
    token_createt = models.IntegerField(null=True)
    api_url = models.CharField(max_length=30,unique=True,null=False)

    def to_json(self):
        return {
            "id": self.id,
            "app_name":self.app_name,
            "api_user":self.api_user,
            "api_token": self.api_token,
            "token_createt":self.token_createt,
            "api_paas": self.api_paas,
            "api_url": self.api_url
        }

# salt-key
class SaltKey(models.Model):
    key_name =  models.CharField(max_length=30,unique=True)
    key_status = models.CharField(max_length=30)

    def to_json(self):
        return {
            "id": self.id,
            "key_name":self.key_name,
            "key_status":self.key_status,
        }

# deloy log
class DeployLog(models.Model):
    deploy_target =  models.CharField(max_length=30)
    deploy_app = models.CharField(max_length=30)
    deploy_time = models.DateTimeField(auto_now_add=True)
    deploy_user = models.CharField(max_length=30)
    deploy_jid = models.CharField(max_length=50)

    def to_json(self):
        return {
            "id": self.id,
            "deploy_target": self.deploy_target,
            "deploy_app":self.deploy_app,
            "deploy_time":self.deploy_time,
            "deploy_user": self.deploy_user,
            "deploy_jid": self.deploy_jid
        }

# runcmd log
class RuncmdLog(models.Model):
    runcmd_target =  models.CharField(max_length=30)
    runcmd_cmd = models.CharField(max_length=30)
    runcmd_time = models.DateTimeField(auto_now_add=True)
    runcmd_user = models.CharField(max_length=30)
    runcmd_result = models.TextField(max_length=10000000)

    def to_json(self):
        return {
            "id": self.id,
            "runcmd_target": self.runcmd_target,
            "runcmd_cmd":self.runcmd_cmd,
            "runcmd_time":self.runcmd_time,
            "runcmd_user": self.runcmd_user,
            "runcmd_result": self.runcmd_result
        }

# 维护操作
class MatTask(models.Model):
    mattask_name =  models.CharField(max_length=30)
    mattask_user = models.CharField(max_length=30)
    mattask_jid = models.CharField(max_length=30)
    mattask_creattime = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            "id": self.id,
            "mattask_name": self.mattask_name,
            "mattask_user": self.mattask_user,
            'mattask_jid': self.mattask_jid,
            "mattask_creattime": self.mattask_creattime,
        }


class AppPermissions(models.Model):
    pass
