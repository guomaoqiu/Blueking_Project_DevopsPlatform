# -*- coding: utf-8 -*-
from celery import task
from sendmessage import send
from common.log import logger
from celery.schedules import crontab
from celery.task import periodic_task
import time

##########################################################################################################
# 周期任务 : 每一分钟发送一封邮件，这里使用邮件发送的方式。
@periodic_task(run_every=crontab(minute='*', hour='*', day_of_week="*"))
def sendmessage():
    """
    @summary: 发送邮件的任务函数
    @note: Celery 启动后，该任务会自动注册到djcelery的库中
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mail_title = u'Blueking Info'
    mailto_list = ['807358130@qq.com']  ## 如果有多个用户请以分号分隔.
    mail_content = u"辛苦了，继续加油! {}".format(now)

    # 执行发送邮件操作....
    try:
        s = send.SendMail()
        s.send_mail(to_list=mailto_list,sub=mail_title,content=mail_content)
        logger.info(u"celery 周期任务调用成功，当前时间：{}".format(now))
        print 'Send Success...',
    except Exception,e:
        print 'Send Failed!',e
        logger.error(u"收集失败，当前时间：{}".format(now))
    return 'sendmessage is ok'