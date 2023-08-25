import smtplib;
import configparser
from email.mime.text import MIMEText
from email.header import Header

#from bnu import is_bnu_studentid;

cf=configparser.ConfigParser()
cf.read("settings.ini")

smtp_obj = smtplib.SMTP_SSL(cf.get('mail', 'smtp_addr'), cf.get('mail', 'smtp_port'))
smtp_obj.login(cf.get('mail', 'address'), cf.get('mail', 'passwd'))

sender = cf.get('mail', 'address')



def send_mail(receiver, title, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = 'verify'; #Header("验证码verify code", 'utf-8')   # 发送者
    # message['To'] =  Header(receiver, 'utf-8');       # 接收者
    message['To'] = receiver;       # 接收者
    message['Subject'] = Header(title, 'utf-8')
    try:
        print(message.as_string())
        smtp_obj.sendmail(sender, receiver, message.as_string())
        return True
    except:
        return False
    pass






#send_mail(test_receivers, '测试标题', 'test content')
