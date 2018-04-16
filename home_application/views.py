# -*- coding: utf-8 -*-
import json, time, celery,simplejson
from django.http  import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from common.log import logger
from common.mymako import render_mako_context, render_json
from models import Hostinfo ,ApiMg, SaltKey, DeployLog,RuncmdLog,MatTask
from saltapi.saltapi import SaltApi
from settings import PRPCRYPTO_KEY
from djcelery.models import TaskMeta
from crypto import prpcrypt
from check_result import  check_result
from django.conf import settings
import requests
import commands

##############################################

def index(request):
    """
    首页
    """
    # 当登陆成功后记录 session
    request.session['logined'] = 'yes'

    server_count = Hostinfo.objects.count()

    # salt部署日志
    each_deploy = []
    [ each_deploy.append(i.to_json()) for i in DeployLog.objects.order_by("-id") ]
    deploy_list = []
    for each_info in each_deploy:
            each_info["deploy_time"] = each_info['deploy_time'].strftime('%Y-%m-%d %H:%M:%S')
            deploy_list.append(each_info)

    # 命令执行日志
    each_runcmd = []
    [ each_runcmd.append(i.to_json()) for i in RuncmdLog.objects.order_by("-id") ] #按照id倒序
    runcmd_list = []
    for each_info in each_runcmd:
        each_info["runcmd_time"] = each_info['runcmd_time'].strftime('%Y-%m-%d %H:%M:%S')
        runcmd_list.append(each_info)
    return render_mako_context(request, '/home_application/opsplatform/index.html',{"server_count":server_count,"deploy_list":deploy_list,"runcmd_list":runcmd_list})


################ SaltAPI测试 ##################
@csrf_exempt
def get_server_info(request):
    '''
    @note: 通过saltapi获取所有minion主机的服务器信息，填入写入数据库中
    '''
    # 获取所有server的hostname
    if request.method == "POST":
        if len(ApiMg.objects.filter(app_name='saltstack')) == 0:
            result = {"result": False, "message": u'请确保api信息已录入！'}
            return render_json(result)
        else:
            try:
                client = SaltApi('saltstack')
                params = {'client': 'local', 'fun': 'test.ping', 'tgt': '*'}
                json_data = client.get_allhostname(params)

                data = dict(json.loads(json_data)['return'][0])

                hostname_list = []

                [hostname_list.append(i) for i in data.keys()]

                for host in hostname_list:
                    if not Hostinfo.objects.filter(hostname=host):

                        all_host_info = dict(client.get_minions(host).items())
                        host_record = Hostinfo(
                            hostname=all_host_info['hostname'],
                            private_ip=all_host_info['private_ip'],
                            public_ip=all_host_info['public_ip'],
                            mem_total=all_host_info['mem_total'],
                            cpu_type=all_host_info['cpu_type'],
                            num_cpus=all_host_info['num_cpus'],
                            os_release=all_host_info['os_release'],
                            kernelrelease=all_host_info['kernelrelease']
                        )

                        host_record.save()

                result = {"result": True, "message": u'刷新完毕！'}
                return render_json(result)

            except Exception, e:
                result = {"result": False, "message": u'刷新出错！'}
                return render_json(result)

def server_list(request):
    """
    从数据库中读取
    """
    host_list = Hostinfo.objects.all()
    data = []
    [ data.append(i.to_json()) for i in host_list ]
    return render_mako_context(request, '/home_application/opsplatform/server_list.html',{"data":data})

@csrf_exempt
def delete_server(request):
    '''
    @note: 从数据库中删除已经存在的主机
    '''
    delete_host = []
    [ delete_host.append(host.encode('raw_unicode_escape')) for host in (request.GET.get('host').split(','))]

    try:
        [ Hostinfo.objects.filter(hostname=host).delete() for host in delete_host ]
        result = {'result': True, 'message': u"删除所选主机成功" }
    except Exception, e:
        logger.error(u"删除所选主机失败,%s" % e)
        result = {'result': False, 'message': u"删除所选主机失败,%s" % e}
    return render_json(result)

def display_hostdetail(request):
    '''
    @note: 通过数据库查询指定主机的详细信息
    '''
    detail_host = request.GET.get('host')
    host_list = Hostinfo.objects.filter(hostname=detail_host)
    data = []
    [data.append(i.to_json()) for i in host_list]
    return render_mako_context(request, '/home_application/opsplatform/host_detail.html',{'data':data})

@csrf_exempt
def api_connect(request):
    '''
    @note: 添加api的信息
    '''
    data = []
    if request.method == 'POST':
        if request.POST.get('username', '') == '' or request.POST.get('password', '') == '' or request.POST.get('url', '') == '':
            return render_mako_context(request, '/home_application/opsplatform/api_connect.html', {'res': True})
        else:
            try:
                salt = ApiMg(
                               app_name=request.POST.get('appname', ''),
                               api_user=request.POST.get('username',''),
                               api_paas=request.POST.get('password', ''),
                               api_url=request.POST.get('url', ''),
                               token_createt=int(time.time()),
                               api_token = ''
                               )
                # api密码加密
                prpcrypt_key = prpcrypt(PRPCRYPTO_KEY)
                salt.api_paas = prpcrypt_key.encrypt(request.POST.get('password', ''),)
                salt.save()
                return redirect(reverse('home_application.views.api_connect')) # 重定向
            except Exception,e:
                print e
                return redirect(reverse('home_application.views.api_connect'))
    else:
        salt =  ApiMg.objects.all()
        [ data.append(i.to_json()) for i in salt]
        if len(data) == 0:
            return render_mako_context(request, '/home_application/opsplatform/api_connect.html',{'result':False})
        else:
            for api_info  in data:
                api_info['api_paas'] = '************'
            return render_mako_context(request, '/home_application/opsplatform/api_connect.html',{'result': True, 'data': data})

@csrf_exempt
def add_apiinfo(request):
    '''
    @note: addinfo 页面返回
    '''
    return render_mako_context(request, '/home_application/opsplatform/add_apiinfo.html')


@csrf_exempt
def del_apiinfo(request):
    '''
    @note: 从数据库中删除已经存入的API信息
    '''
    delete_api = request.GET.get('apiid')
    try:
        ApiMg.objects.filter(id=delete_api).delete()
        result = {'result': True, 'message': u"API信息删除成功."}
    except Exception, e:
        logger.error(u"API信息删除失败，%s" % e)
        result = {'result': False, 'message': u"API信息删除失败，%s" % e}
    return render_json(result)

@csrf_exempt
def saltkey_list(request):
    '''
    @note: 从数据库中删除已经存入的API信息
    '''
    data = []
    [data.append(i.to_json()) for i in SaltKey.objects.all()]

    if request.method == "POST":
        if len(ApiMg.objects.filter(app_name='saltstack')) == 0:
            result = {"result": False, "message": u'请确保api信息已录入！'}
            return render_json(result)
        else:
            try:
                client = SaltApi('saltstack')
                params = {'client': 'wheel', 'fun': 'key.list_all'}
                json_data = dict(json.loads(client.saltCmd(params=params))['return'][0])['data']['return']
                # 已经认证的key入库，并将状态设置为Online
                for key_name in  json_data["minions"]:
                    salt_key = SaltKey(key_name=key_name,key_status='Online')
                    salt_key.save()
                # 未认证的key入库，并将状态设置为Offline
                for key_name in json_data["minions_pre"]:
                    salt_key = SaltKey(key_name=key_name, key_status='Offline')
                    salt_key.save()
                result = {'result': True, 'message': u"刷新列表成功."}
            except Exception, e:
                logger.error(u"刷新salt-key列表失败，%s" % e)
                result = {'result': False, 'message': u"刷新列表失败，%s" % e}
            return render_json(result)
    return render_mako_context(request,'/home_application/opsplatform/saltkey_list.html' ,{"data":data})

@csrf_exempt
def salt_minion_test(request):
    '''
    @note: 单台salt-minion测试连通性
    '''
    salt_key = request.GET.get('saltkey')
    try:
        client = SaltApi('saltstack')
        params = {'client': 'local', 'fun': 'test.ping','tgt': salt_key}
        json_data = dict(json.loads(client.saltCmd(params=params)))['return'][0]
        res = json_data[salt_key]
        if res:
            result = {'result': res, 'message': u"该Salt-minion连接正常\n%s" % str(salt_key) }
            return render_json(result)
    except Exception, e:
        logger.error(u"该Salt-minion连接异常\n%s," % e)
        result = {'result': False, 'message': u"该Salt-minion连接异常\n%s," % e}
        return render_json(result)

@csrf_exempt
def del_saltkey(request):
    '''
    @note: 从数据库中删除saltkey
    '''
    del_saltkey = []
    [ del_saltkey.append(host.encode('raw_unicode_escape')) for host in (request.GET.get('saltkey').split(','))]
    try:
        [ SaltKey.objects.filter(key_name=key_name).delete() for key_name in del_saltkey ]
        result = {'result': True, 'message': u"删除saltkey成功\n%s" % str(del_saltkey) }
    except Exception, e:
        logger.error(u"删除saltkey失败，%s" % e)
        result = {'result': False, 'message': u"删除saltkey失败，%s" % e}
    return render_json(result)

@csrf_exempt
def salt_cmd(request):
    '''
    @note: 选择一台server只有执行salt命令; 此函数只能针对一台server进行操作
    '''
    hostname = request.GET.get('hostname','')
    if request.method == 'POST':  # 如何接收ajax post 过来的josn数据...
        data = dict(request.POST)
        # 获取web端输入的命令
        run_cmd = data["cmd"][0]
        cmd = run_cmd.replace("&nbsp;"," ")
        # 命令黑名单
        black_cmd = ['date','echo','rm -rf /','shutdown','poweroff','reboot']
        for s in black_cmd:

            if cmd  in  s:
                result = {"result": False,"message": u'禁止在此平台运行该命令'}
                return render_json(result)
        # 获取主机名
        hostname = data["hostname"][0]

        cmd_params = {'client': 'local', 'fun': 'cmd.run', 'tgt': '%s' % hostname, 'arg': '%s' % cmd}
        try:
            client = SaltApi('saltstack')
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            result_data = dict(dict(json.loads(client.saltCmd(cmd_params)))['return'][0]).values()[0]
            #result_data = dict(json.loads(client.saltCmd(cmd_params)))
            print result_data


            for i in check_result():
                if i in result_data:
                    result = {"result": False, "message": u'执行失败,{0}'.format(i)}
                    return render_json(result)
                else:
                    runcmd_log = RuncmdLog(runcmd_target=hostname,runcmd_cmd=cmd, runcmd_user=request.user,runcmd_result=result_data)
                    runcmd_log.save()
                    result = {"result": True,"data": result_data,"run_time": t,"message": u'执行成功'}
                    return render_json(result)
        except Exception,e:
            logger.info('执行失败')
            result = {"result": False, "message": u'执行失败.{0}'.format(e)}
            print e
            return render_json(result)
    return render_mako_context(request,'/home_application/opsplatform/saltcmd.html',{"hostname":hostname})

def runcmd(request):
    return render_mako_context(request, '/home_application/opsplatform/runcmd.html')

def get_task_history(request):
    '''
    @note: 获取执行的任务历史记录
    '''
    each_data = []
    [ each_data.append(each_task.to_dict()) for each_task in TaskMeta.objects.order_by('-id') ]
    data = []
    for each_info in each_data:
        each_info["date_done"] = each_info['date_done'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(each_info)
    return render_mako_context(request, '/home_application/opsplatform/task_history.html', {"data": data})


def test(request):
    return render_mako_context(request, '/home_application/opsplatform/dingshiqi.html')

def test_get(request):
    import time
    import random
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    num = random.randint(0, 100000)

    data = {"time": t,
            "num": str(num)}
    result_json = json.dumps(data)
    return render_json(result_json)


def run(request):

    return render_mako_context(request, '/home_application/opsplatform/run.html')


@csrf_exempt
def del_runcmd_log(request):
    '''
    @note: 删除所有日志记录
    '''
    if request.method == 'POST':
        logtype = request.GET.get("logtype")
        if logtype == "runcmd":
            try:
                RuncmdLog.objects.all().delete()
                result = {'result': True,'message':u'删除所有命令执行日志成功...'}
                return render_json(result)
            except Exception,e:
                result = {'result': False,'message':u'删除所有命令执行日志失败...\n{0}'.format(e)}
                return render_json(result)
        elif logtype == "deploy":
            try:
                DeployLog.objects.all().delete()
                result = {'result': True, 'message': u'删除所有部署日志成功...'}
                return render_json(result)
            except Exception, e:
                result = {'result': False, 'message': u'删除所有部署日志失败...\n{0}'.format(e)}
                return render_json(result)
        else:
            pass

######################## 后台普通任务执行 ##########################
def task_center(request):
    '''
    @note: 任务中心
    '''
    return render_mako_context(request, '/home_application/opsplatform/task_center.html')

@csrf_exempt
def execute_task(request):
    """
    @summary: 请求函数入口
    """
    if request.method == 'POST':

        res1 = long_time_def.apply_async()
        #string = u'你提交的任务正在后台执行......'
        #
        data = {
            "task_id": res1.id,
            "task_status": res1.status
        }
        #print json.dumps(data)
        string = ''
        print '返回信息: ',data
        result = {"result":True,"data":data,"message":u'哈哈'}
        return render_json(result)
        #return render_mako_context(request, '/home_application/opsplatform/excue_task.html',{'string': string,"result":result})


    return render_mako_context(request, '/home_application/opsplatform/task_center.html')

# @celery.task()
# def custom_task():
#     """
#     @summary: 自定义逻辑
#     """
#     # 定义自己的任务逻辑(比如大数据的计算等...)
#     startime = time.time()             # 记录该逻辑代码起始时间
#     logger.info(u"普通任务开始执行...{}".format(startime))
#     time.sleep(3)
#     res = 'test'
#     endtime = time.time()               # 记录该逻辑代码结束时间
#     logger.info(u"普通任务结束执行...{}".format(endtime))
#
#     usetime = endtime - startime       # 计算该逻辑代码执行耗时
#
#     logger.info(u"普通任务执行完毕，耗时：{}".format(usetime)) # 在 celery 执行过程中记录该消息!
#     return res



@celery.task(bind = True)
def long_time_def(self):
    '''
    @note: 任务进度
    '''
    startime = time.time()  # 记录该逻辑代码起始时间
    logger.info(u"普通任务开始执行...{}".format(startime))
    ##################################################
    # 不可删除,任务进度所需要的
    i = 0
    while i < 100:
        i+= 1

        # 自定义状态
        self.update_state(state='PROGRESS',meta={'i':i})
        #time.sleep(0.2)
    ##################################################

    # 此处写任务逻辑i
        #time.sleep(0.2)
        time.sleep(0.2)
        #commands.getoutput("ping -c 3 www.baidu.com")
        self.update_state(state='PENDING',meta={'i':i})

        # client = SaltApi('saltstack')
        # params = {'client': 'local', 'fun': 'cmd.run', 'tgt': '*', 'arg': 'free'}
        # json_data = json.loads(client.saltCmd(params=params)
        #print json_data

        #json_data = dict(json.loads(client.saltCmd(params=cmd_params))['return'][0])['data']['return']
        #import commands
        #commands.getoutput("ping -c 10 www.baidu.com")
    endtime = time.time()  # 记录该逻辑代码结束时间
    logger.info(u"普通任务结束执行...{}".format(endtime))
    usetime = endtime - startime  # 计算该逻辑代码执行耗时
    logger.info(u"普通任务执行完毕，耗时：{}".format(usetime))  # 在 celery 执行过程中记录该消息!


    return 'finished'

@csrf_exempt
def task_result_test(request):
    import commands
    if request.method == 'POST':
        data = commands.getoutput('date')
        result = {"result": True, 'data':data}
        return render_json(result)

def task_result(request):
    '''
    @note: 通过task_id 来获取任务状态
    '''
    task_id = request.GET.get('task_id')
    print task_id
    from celery.result import AsyncResult
    the_task = AsyncResult(task_id)

    print("任务：{0} 当前的 state 为：{1}".format(task_id, the_task.state))

    # print the_task.info.get('i',0)
    if  the_task.state  == 'PROGRESS':
        print the_task.info.get('i', 0)
        result = {'state': 'progress','progress':the_task.info.get('i',0)}
    elif  the_task.state  == 'SUCCESS':
        result = {'state': "success", 'progress':100}
    elif  the_task.state  == 'PENDING':
        result = {'state': 'waitting', 'progress':0}
    elif  the_task.state  == 'FA':
        result = {'state': 'waitting', 'progress':0}
    else:
        result = {'state': the_task.state,'progress':the_task.info.get('i',0) }
    return render_json(result)


#################### 应用部署 ###################
@csrf_exempt
def soft_deploy(request):
    '''
    @note: 应用部署
    '''
    # 获取所有主机
    host_list = Hostinfo.objects.all()
    all_host = []
    [ all_host.append(i.to_json()['hostname']) for i in host_list ]

    # 定义state
    soft = ["nginx","zabbix_client","redis","Mongodb"]

    if request.method == "POST":
        data = dict(request.POST)
        # 主机列表
        host_list = []
        [host_list.append(each_host) for each_host in  list(data['host_arr'])[0].split(',')]

        # 软件列表
        soft_list = []
        [soft_list.append(each_soft) for each_soft in list(data['soft_arr'])[0].split(',')]

        deploy_info = []

        sum = 0
        client = SaltApi('saltstack')
        for each_host in host_list:
            for each_soft in soft_list:
                sum+=1
                deploy_parmas = {'client': 'local_async', 'fun': 'state.sls', 'tgt': each_host,'arg': each_soft}
                jid = dict(json.loads(client.saltCmd(params=deploy_parmas))['return'][0]).values()[0]
                deploy_info.append({"msg": "%s ==>> %s" % (each_host,each_soft), "id":sum,"job_id":jid})
                # 部署信息入库
                deploy_log = DeployLog(deploy_app=each_soft,deploy_target=each_host,deploy_time=int(time.time()),deploy_user=request.user,deploy_jid=jid)
                deploy_log.save()
        result = {"result":True,"data":deploy_info}
        #print deploy_info
        return render_json(result)
    return render_mako_context(request, '/home_application/opsplatform/soft_deploy.html',{"all_host":all_host,"soft":soft})


@csrf_exempt
def get_jid_result(request):
    '''
    @note: 获取salt任务的执行结果
    '''
    job_id = request.GET.get('jid','')

    client = SaltApi('saltstack')
    result = client.get_jid_result(job_id)

    fail_list = ['command not found','error']

    for i in fail_list:
        if i in result:

    #result = dict(json.loads(client.get_jid_result(job_id)))['info']  # salt_2016.11.1 新版本使用该语句
    # result = json.loads(client.get_jobs(JID))['return'][0]['data'] # salt_2015.5.10 老版本使用该语句
            return HttpResponse("执行失败！")

@csrf_exempt
def salt_jid_result(request):
    '''
    @note: 获取salt任务的执行结果
    '''
    job_id = request.GET.get('jid', '')

    try:
        client = SaltApi('saltstack')
        result_data = dict(json.loads(client.get_jid_result(job_id))['info'][0])['Result']
        result = simplejson.dumps(result_data,sort_keys=True, indent='    ')
        return render_mako_context(request, '/home_application/opsplatform/salt_jid_result.html',{"result":result})
    except Exception,e:
        result = e
        return render_mako_context(request, '/home_application/opsplatform/salt_jid_result.html',{"result":result})


def send_key(request):
    '''
    @ note：用于发送执行类的KEY密码:
    '''
    import requests
    #URL = "http://114.55.0.47:9999/openqq/send_friend_message"  # 这里发送的是好友
    URL =   "http://114.55.0.47:9999/openqq/send_group_message" # 这里发送的是群

    data = {
        "uid": request.GET.get('id'),
        "content": request.GET.get('content'),
    }
    result=requests.get(url=URL, data=data)
    return HttpResponse(result)


##### 维护
@csrf_exempt
def online_maintain(request):
    task_name = {
        1: u'全服停服',
        2: u'IOS停服',
        3: u'安卓停服',
        4: u'缓存清理',
        5: u'配置发布',
        6: u'代码拉取',
        7: u'全服开服',
        8: u'IOS开服',
        9: u'安卓开服',
    }
    if request.method == 'POST':

        task_id = request.GET.get('task_id')

        for k,v in task_name.items():

            if int(k) == int(task_id):
                print '你将执行的操作是: ',v
                try:
                    client = SaltApi('saltstack')
                    deploy_parmas = {'client': 'local_async', 'fun': 'cmd.run', 'tgt': '*', 'arg': 'sh /root/a.sh'}
                    jid = dict(json.loads(client.saltCmd(params=deploy_parmas))['return'][0]).values()[0]

                    # 入库
                    mattask = MatTask(mattask_name=v, mattask_user=request.user,mattask_jid=jid)
                    mattask.save()

                    result = {'result':True,'message':u'{0} 任务已经下发，后台执行中...'.format(v)}
                    return render_json(result)
                except Exception,e:
                    result = {'result':False,'message':u'{0} 执行失败\n{1}'.format(v,e)}
                    return render_json(result)
    jid = ''
    each_mat = []
    [each_mat.append(i.to_json()) for i in MatTask.objects.order_by("-id")]
    data = []
    for each_info in each_mat:
        each_info["mattask_creattime"] = each_info['mattask_creattime'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(each_info)
    return render_mako_context(request, '/home_application/opsplatform/online_maintain.html',{'task_name':task_name.items(),'jid':jid,'data':data})


@csrf_exempt
def del_maintain_log(request):
    '''
    @note: 维护日志清理
    '''
    if request.method == 'POST':
        try:
            MatTask.objects.all().delete
            result = {"result": True,'message':u'清理完毕...'}
            return render_json(result)
        except Exception,e:
            result = {"result": False,'message':u'清理清理失败{}'.format(e)}
            return render_json(result)


############# saltstack ################

def action_saltcmd(request):
    '''
    @note： 指定单台或者多台服务器批量执行命令
    '''
    #print request.
    return render_mako_context(request, '/home_application/opsplatform/action_saltcmd.html')
