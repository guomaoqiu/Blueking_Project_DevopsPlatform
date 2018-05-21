# -*- coding: utf-8 -*-

url = "https://www.okcoin.cn/api/v1/ticker.do?symbol=ltc_cny"

import  requests,json
head = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'}

con = requests.get(url,headers=head)

import time


import smtplib
from email.mime.text import MIMEText

import commands

class SendMail():
    def __init__(self):
        self.__mail_host = 'smtp.qq.com'
        self.__mail_port = '465'
        self.__mail_user = '2399447849'
        self.__mail_pass = ''
        self.__mail_postfix = 'qq.com'


    def send_mail(self,to_list,sub,content):
        me="-"+"<"+self.__mail_user+"@"+self.__mail_postfix+">"
        msg = MIMEText(content,_subtype='html',_charset='utf8')
        msg['Subject'] = sub
        msg['From']=me
        msg['to']=";".join(to_list)
        s = smtplib.SMTP_SSL()
        s.connect(self.__mail_host)
        s.login(self.__mail_user,self.__mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()



if __name__ == "__main__":
    # 初始化
    s = SendMail()

    # 发送列表
    mailto_list = ['2399447849@qq.com']

    each = json.loads(con.text)["ticker"]["last"]
    #print each
    #print float(55.92) * float(each)
    #print "test: %s" % each
    s.send_mail(to_list=mailto_list,content='',sub="成交: %s 总额: %s 亏损: %s ----- %s " % (float(each),
                                                                                            float(55.92) * float(each),
                                                                                            int(20000) - float(each) * float(55.92),
                                                                                            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                                                                            )
                )









