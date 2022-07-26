import re
import smtplib
import imaplib
import email
import time
from datetime import datetime
from email.header import decode_header
from config import mail_setting


class Email:

    def __init__(self):
        self.sendtime = self.test_sendmail()
        time.sleep(3)  # 等待信件寄送並收到的時間
        self.M = self.get_mail()
        self.subject_list = self.get_subject_list()
        self.findmail = self.find_mail()
        self.delete_testmail()
        self.M.close()
        self.M.logout()

    def test_sendmail(self):  # 寄信件標題為YYYYMMDD_HHMM的測試信件
        smtp = smtplib.SMTP(mail_setting['server'])
        subject = datetime.now().strftime("%Y%m%d_%H%M")
        message = 'Subject: {}\n\n{}'.format(subject, 'test')
        smtp.sendmail(mail_setting['sender'], mail_setting['address'], message)
        smtp.quit()
        return subject

    def get_mail(self):  # 帳密登入後回傳信箱
        M = imaplib.IMAP4(mail_setting['server'])
        M.login(mail_setting['account'], mail_setting['pwd'])
        M.select()
        return M

    def get_subject_list(self):  # 取得信件與標題的list
        subject_list = []
        typ, data = self.M.search(None, 'ALL')
        for num in data[0].split():
            typ, data = self.M.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject = msg.get('subject')
            text, encoding = decode_header(subject)[0]
            try:
                title = text.decode('UTF-8')
            except (UnicodeDecodeError, AttributeError):
                title = text
            finally:
                subject_list.append((num, title))
        return subject_list

    def find_mail(self):  # 檢查信箱是否有信件標題為剛剛寄送的YYYYMMDD_HHMM的測試信件
        mail_subject_list = [x[1] for x in self.subject_list]
        if self.sendtime in mail_subject_list:
            return True
        else:
            return False

    def delete_testmail(self):  # 只保留當天的測試信，其它全刪
        today = datetime.now().strftime("%Y%m%d")
        for num, subject in self.subject_list:
            if re.match('[0-9]{8}_', subject[0:9]):
                if subject[0:8] != today:
                    self.M.store(num, '+FLAGS', '\\Deleted')
        self.M.expunge()

    @staticmethod
    def email_valid(email):  # 回傳email格式是否有效
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False


if __name__ == '__main__':
    ### 回傳email格式是否有效
    # print(Email.email_valid('ysuper@automodules.com'))
    # print(Email.email_valid('ysuper@automodules'))

    ### 測試寄信功能
    print(Email().findmail)
