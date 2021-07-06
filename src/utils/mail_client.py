# coding:utf -8

import smtplib  # smtp服务器
from email.mime.text import MIMEText  # 邮件文本

class MailClient:

    # 保存数据
    def send(self, subject, content):
        sender = "ranmaxli_test@163.com"  # 发送方
        recver = "1206038126@qq.com"  # 接收方
        password = "jTdu1q3xJqW8c2nz"
        message = MIMEText(content, "plain", "utf-8")

        message['Subject'] = subject  # 邮件标题
        message['To'] = recver  # 收件人
        message['From'] = sender  # 发件人

        smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
        smtp.login(sender, password)  # 发件人登录
        smtp.sendmail(sender, [recver], message.as_string())  # as_string 对 message 的消息进行了封装
        smtp.close()


mail_client = MailClient()