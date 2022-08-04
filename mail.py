#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import logging
# 第三方 SMTP 服务

my_sender='845809341@qq.com'    # 发件人邮箱账号
my_pass="njazwgvnroznbcai"   #口令
my_user=['845809341@qq.com']      # 收件人邮箱账号，我这边发送给自己


def mail(u,datas):
        ret=True
    # for u in my_user:
        try:
            mes_str=datas
            msg=MIMEText(mes_str,_subtype="html",_charset='utf-8')
            msg['From']=formataddr(["Vision",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["Vision",u])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="事业单位岗位监控邮件"                # 邮件的主题，也可以说是标题

            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[u,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            logging.exception(e)
            ret=False
        return ret
def get_html(data_list):
    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>'
    th = "<body text='#000000'><center><font size=5 color='#dd0000'><b>" + "今日更新岗位数:" + str(len(data_list)) + "</b></font></center>" \
     "<br/><table style=' font-size: 14px;' border='1' cellspacing='0' cellpadding='1' bordercolor='#000000' width='20%' align='center' ></table>" \
     "<br/><table bgcolor='#B0E0E6' style=' font-size: 14px;'border='1' cellspacing='0' cellpadding='0' bordercolor='#000000' width='95%' align='center' >" \
      "<tr  bgcolor='#F79646' align='left' >" \
      "<th>日期</th>" \
      "<th>岗位</th>" \
      "<th>地方</th>" \
        "</tr>"
    tr = ""
    for row in data_list:
        td = ''
        td = td + "<td>" + str(row["update_date"]) + "</td>"
        td = td + "<td><a href='" +str(row["job_url"])+"'>"+ str(row["job_name"]) + "</ a></td>"
        td = td + "<td>" + str(row.get("city")) + "</td>"
        tr = tr + "<tr>" + td + "</tr>"
    body = str(tr)
    tail = '</table></body></html>'
    mail_str = header + th + body + tail
    return mail_str
