# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsJOB(object):
    """Collections of JOB APIS"""

    def __init__(self, client):
        self.client = client

        self.execute_task = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/job/execute_task/',
            description=u'根据作业模板ID启动作业',
        )
        self.fast_execute_script = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/job/fast_execute_script/',
            description=u'快速执行脚本',
        )
        self.fast_push_file = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/job/fast_push_file/',
            description=u'快速分发文件',
        )
        self.get_agent_status = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/job/get_agent_status/',
            description=u'查询Agent状态',
        )
        self.get_task_detail = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/job/get_task_detail/',
            description=u'查询作业模板详情',
        )
        self.get_task_ip_log = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/job/get_task_ip_log/',
            description=u'根据作业实例ID查询作业执行日志',
        )
        self.get_task_result = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/job/get_task_result/',
            description=u'根据作业实例 ID 查询作业执行状态',
        )
