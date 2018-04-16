# -*- coding: utf-8 -*-

"""
mako模板的render方法等
"""

import json
from django.conf import settings
from django.http import HttpResponse
from django.template.context import Context
from mako.lookup import TemplateLookup
from common.log import logger


"""
mylookup 也可以单独使用：
@Example:
             mako_temp = mylookup.get_template(template_name)
             mako_temp.render(**data)
"""
mylookup = TemplateLookup(directories=settings.MAKO_TEMPLATE_DIR,
                          module_directory=settings.MAKO_TEMPLATE_MODULE_DIR,
                          output_encoding='utf-8',
                          input_encoding='utf-8',
                          encoding_errors='replace',
                          collection_size=500,
                          )


def render_mako(template_name, dictionary={}, context_instance=None):
    """
    render the mako template and return the HttpResponse

    @param template_name: 模板名字
    @param dictionary: context字典
    @param context_instance: 初始化context，如果要使用 TEMPLATE_CONTEXT_PROCESSORS，则要使用RequestContext(request)
    @note: 因为返回是HttpResponse，所以这个方法也适合给ajax用(dataType不是json的ajax)
    @Example:
                 render_mako('mako_temp.html',{'form':form})
            or
                 render_mako('mako_temp.html',{'form':form},RequestContext(request))
            or
                 render_mako('mako_temp.html',{},RequestContext(request，{'form':form}))
    """

    mako_temp = mylookup.get_template(template_name)
    if context_instance:
        # RequestContext(request)
        context_instance.update(dictionary)
    else:
        # 默认为Context
        context_instance = Context(dictionary)
    data = {}
    # construct date dictory
    for d in context_instance:data.update(d)
    # return response
    return HttpResponse(mako_temp.render_unicode(**data))   # .replace('\r','').replace('\n','').replace('\t','')


def render_mako_context(request, template_name, dictionary={}):
    """
    render the mako template with the RequestContext and return the HttpResponse
    """
    context_instance = get_context_processors_content(request)
    # ===========================================================================
    # # you can add csrf_token here
    # from django.core.context_processors import csrf
    # context_instance['csrf_token'] = csrf(request)['csrf_token']
    # ===========================================================================
    # render
    return render_mako(template_name, dictionary=dictionary, context_instance=context_instance)


def render_mako_tostring(template_name, dictionary={}, context_instance=None):
    """
    render_mako_tostring without RequestContext
    @note: 因为返回是string，所以这个方法适合include的子页面用
    """
    mako_temp = mylookup.get_template(template_name)
    if context_instance:
        # RequestContext(request)
        context_instance.update(dictionary)
    else:
        # 默认为Context
        context_instance = Context(dictionary)
    data = {}
    # construct date dictory
    for d in context_instance:
        data.update(d)
    # return string
    return mako_temp.render_unicode(**data)     # .replace('\t','').replace('\n','').replace('\r','')


def render_mako_tostring_context(request, template_name, dictionary={}):
    """
    render_mako_tostring with RequestContext
    """
    context_instance = get_context_processors_content(request)
    return render_mako_tostring(template_name, dictionary=dictionary, context_instance=context_instance)


def render_json(dictionary={}):
    """
    return the json string for response
    @summary: dictionary也可以是string, list数据
    @note:  返回结果是个dict, 请注意默认数据格式:
                                    {'result': '',
                                     'message':''
                                    }
    """
    if type(dictionary) is not dict:
        # 如果参数不是dict,则组合成dict
        dictionary = {
            'result': True,
            'message': dictionary,
        }
    return HttpResponse(json.dumps(dictionary), content_type='application/json')


def get_context_processors_content(request):
    """
    return the context_processors dict context
    """
    context = Context()
    try:
        from django.utils.module_loading import import_string
        from django.template.context import _builtin_context_processors
        context_processors = _builtin_context_processors
        for i in settings.TEMPLATES:
            context_processors += tuple(i.get('OPTIONS', {}).get('context_processors', []))
        cp_func_list = tuple(import_string(path) for path in context_processors)
        for processors in cp_func_list:
            context.update(processors(request))
    except Exception, e:
        logger.error(u"Mako: get_context_processors_content error info:%s" % e)
        context = Context()
    return context
