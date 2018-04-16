# -*- coding: utf-8 -*-

from django.utils import timezone
from django.db import models
from common.log import logger


class Function_Manager(models.Manager):
    def func_check(self, func_code):
        """
        @summary: 检查改功能是否开放
        @param func_code: 功能ID
        @return: (True/False, 'message')
        """
        try:
            enabled = self.get(func_code=func_code).enabled
            return (True, int(enabled))
        except Exception, e:
            logger.error(u"检查改功能是否开放发生异常，错误信息：%s" % e)
            return (False, 0)


class Function_controller(models.Model):
    """
    功能开启控制器
    """
    func_code = models.CharField(u"功能code", max_length=64, unique=True)
    func_name = models.CharField(u"功能名称", max_length=64)
    enabled = models.BooleanField(u"是否开启该功能", help_text=u"控制功能是否对外开放，若选择，则该功能将对外开放", default=False)
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)
    func_developer = models.TextField(u"功能开发者", help_text=u"多个开发者以分号分隔", null=True, blank=True)
    objects = Function_Manager()

    def __unicode__(self):
        return self.func_name

    class Meta:
        app_label = 'app_control'
        verbose_name = u"功能控制器"
        verbose_name_plural = u"功能控制器"
