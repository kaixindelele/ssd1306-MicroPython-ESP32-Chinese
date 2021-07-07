#!usr/bin/env python 
# -*- coding:utf-8 -*- 
"""
@file: emailHandler.py
@time: 2018/04/21
"""
# 邮件服务封装
 
import smtplib
 
 
class EmailHandler(object):
 
    def __init__(self, 
                 user='myqqnum', 
                 password='asndsfdsfewweg', 
                 ):
        """
        :param user:str 发送人邮箱地址（用户名）
        :param password:str 发送人申请的    !!!授权码!!!   需要登录邮箱后在
设置里拿到授权码
        """
        self.__QQ = {'smtp': 'smtp.qq.com', 'port': 465}        
        self.user = user
        self.password = password        
        self.server = smtplib.SMTP_SSL(self.__QQ['smtp'], self.__QQ['port']
)
        self.server.ehlo()
        self.server.login(self.user, self.password)
        
    def send_mail(self, to, subject, content=None):
        """
        :param to:str 接收人邮箱地址
        :param subject:str 邮件标题
        :param content:str 邮件内容
        """        
        self.server.sendmail(self.user+'@qq.com',
                             to+'@qq.com',
                             'Subject:'+subject+'\nthis is '+content)
                   
          
    def send_error_to_myqq(self,
                           to='myqqnum',
                           subject="Code Error!",
                           content='Cube is out of bound'):
        self.send_mail(to=to, 
                       subject=subject, 
                       content=content)
        
def main():
    email = EmailHandler(user="myqqnum", 
                         password="asndsfdsfewweg", 
                         )

    email.send_error_to_myqq()


if __name__=="__main__":
    main()
