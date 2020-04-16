#coding:utf-8

import os
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib



def is_dev():
	return True if os.getenv('img_crawl_env') == 'dev' else False


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(exception, from_name,to_name,subject):
    from_addr = 'pudge702@qq.com'
    password = 'szohdesuyuwvdifc'
    to_addr = 'pudge702@qq.com'
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(exception, 'plain', 'utf-8')
    msg['From'] = _format_addr('%s <%s>' % (from_name,from_addr))
    msg['To'] = _format_addr('%s <%s>' % (to_name,to_addr))
    msg['Subject'] = Header(subject, 'utf-8').encode()

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        #   server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print('send email success')
    except Exception as e:
        print(str(e))


def exception_alarm(func):
    """异常上报装饰器"""
    import traceback

    def alarm(*args):
        try:
            result = func(*args)
        except Exception:
            traceback.print_exc()
            send_mail(traceback.format_exc(),'jason','jason','exception_alarm')
    return alarm


def xpath_exception_alarm(func):

    def alarm(sel, xpath_rule, xpath_object):
        result = func(sel, xpath_rule, xpath_object)
        # print('result', result)
        if not result:
            send_mail(xpath_object+"__"+xpath_rule, 'jason', 'jason', 'xpath_exception_alarm')
        return result

    return alarm