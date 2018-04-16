# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
    # 主页
    (r'^$', 'index'),
    # saltstack连接相关信息
    (r'^api_connect/$', 'api_connect'),
    # 添加api信息
    (r'^add_apiinfo/$', 'add_apiinfo'),
    # 删除api信息
    (r'^del_apiinfo/$', 'del_apiinfo'),
    # 通过saltapi收集主机信息
    (r'^get_server_info/$', 'get_server_info'),
    # 显示主机详情页
    (r'^display_hostdetail/$', 'display_hostdetail'),
    # 服务器列表
    (r'^server_list/$', 'server_list'),
    # 删除主机
    (r'^delete_server/$', 'delete_server'),
    # 获取主机
    #(r'^get_host/data$', 'get_host'),
    (r'^saltkey_list/$', 'saltkey_list'),
    # 定时器测试
    (r'^test/$', 'test'),
    (r'^test_get/$', 'test_get'),
    (r'^run/$', 'run'),
    # salt-minoin端连接性测试
    (r'^salt_minion_test/$', 'salt_minion_test'),
    # salt-minoin端连接性测试
    (r'^salt_cmd/$', 'salt_cmd'),
    # 删除salt-key
    (r'^del_saltkey/$', 'del_saltkey'),
    # 获取历史任务记录
    (r'^get_task_history/$', 'get_task_history'),
    # 任务中心
    (r'^task_center/$', 'task_center'),
    # 应用部署
    (r'^soft_deploy/$', 'soft_deploy'),
    # 获取salt jid结果
    (r'^salt_jid_result/$', 'salt_jid_result'),
    # salt命令执行(单台server)
    (r'^runcmd/$', 'runcmd'),
    # 删除命令执行日志
    (r'^del_runcmd_log/$', 'del_runcmd_log'),

    # 正式服维护
    (r'^online_maintain/$', 'online_maintain'),
    # 删除所有维护日志
    (r'^del_maintain_log/$', 'del_maintain_log'),

    # salt命令执行:
    (r'^action_saltcmd/$', 'action_saltcmd'),






########### for test ############
    (r'^execute_task/$', 'execute_task'),
    (r'^send_key/$', 'send_key'),

    (r'^task_result/$', 'task_result'),
    (r'^task_result_test/$', 'task_result_test'),
)
