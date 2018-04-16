#! -*- coding:utf-8 -*-
def check_result():
    '''
    @node: 用于salt在执行命令或应用部署时返回的结果进行扫描；包含这些关键字则说明命令执行或应用部署失败.
    :return:
    '''
    error_result = [
        'command not found',
        'error',
        'Error',
        'ERROR'
    ]
    return error_result
