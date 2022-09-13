#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 发件人邮箱账号
SENDER = 'sender@email.com'
SENDER_ALIAS = 'sender'
# user登录邮箱的用户名，password登录邮箱的密码（授权码，即客户端密码，非网页版登录密码），但用腾讯邮箱的登录密码也能登录成功
SENDER_PASSWORD = 'password'
# 收件人邮箱账号
RECEIVER = 'receiver@email.com'


def send_mail():
    try:
        msg = MIMEText('This is a mail from sender by tencent enterprice mail POP3 service', 'plain', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(["xx", SENDER])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(["xx", RECEIVER])
        # 邮件的主题
        msg['Subject'] = "Tencent Enterprice Mail test"

        # SMTP服务器，腾讯企业邮箱端口是465，腾讯邮箱支持SSL(不强制)， 不支持TLS
        # qq邮箱smtp服务器地址:smtp.qq.com,端口号：456
        # 163邮箱smtp服务器地址：smtp.163.com，端口号：25
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        # 登录服务器，括号中对应的是发件人邮箱账号、邮箱密码
        server.login(SENDER, SENDER_PASSWORD)
        # 发送邮件，括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(SENDER, [RECEIVER, ], msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    ret = send_mail()
    if ret:
        print("send mail success")
    else:
        print("send mail fail")