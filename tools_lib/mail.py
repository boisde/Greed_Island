# -*- coding:utf-8 -*-
import traceback
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText


NO_REPLY_MAIL = "no-reply@123feng.com"
MAIL_PASSWD = "fdg2874@xa"
MAIL_HOST = "smtp.exmail.qq.com"


def send_mail(to_addrs, title, body, content_type='plain'):
    """
    邮件发送
    同步发送，功能简陋，以后再升级
    @param to_addrs: 收件地址
    @param title: 标题
    @param body: 正文
    @param content_type: 类型
    @return:
    """
    try:
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

        msg = MIMEText(body, content_type, 'utf-8')
        msg['From'] = NO_REPLY_MAIL
        msg['To'] = ';'.join(to_addrs)
        msg['Subject'] = Header(title, charset='utf-8').encode()

        server = smtplib.SMTP(MAIL_HOST, port=25)
        server.login(NO_REPLY_MAIL, MAIL_PASSWD)
        server.sendmail(NO_REPLY_MAIL, to_addrs=to_addrs, msg=msg.as_string())
        server.quit()
    except:
        print traceback.format_exc()


if __name__ == '__main__':
    send_mail(['sunguyu@123feng.com', 'qianlei@123feng.com'], '测试', 'hello,world\n我是天才')

