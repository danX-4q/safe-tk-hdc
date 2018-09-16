#!/usr/bin/env python2
#-*- coding: utf8 -*-

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import logging

import HdcConst

class CHdcAction:
    def __init__(self, prog_conf):
        self.prog_conf = prog_conf
        self.main_conf = self.prog_conf['action']['mail']
        self.logger = logging.getLogger()

    def sendMail(self, cur_cmd_tt, cmd_run, blocks) :
        try:
            server = smtplib.SMTP_SSL(
                self.main_conf['smtp_host'], 
                self.main_conf['smtp_port'])
            server.login(
                self.main_conf['user'], 
                self.main_conf['password'])

            mail_msg = self.get_attach(cur_cmd_tt, cmd_run, blocks)
            self.logger.info("to send email: %s", mail_msg)

            server.sendmail(
                "<%s>" % self.main_conf['user'], 
                self.main_conf['to'].split(';'), 
                mail_msg
                )
            server.close()
            self.logger.info("send email successful")

        except Exception as e:
            self.logger.error("send email failed %s" % e)

    def get_attach(self, cur_cmd_tt, cmd_run, blocks) :

        if cmd_run == HdcConst.CMD_RUN_ERR :
            message = MIMEText('safe-cli or safed run error', 'plain', 'utf-8')
            message["From"] = Header(self.main_conf['user'], 'utf-8')
            message["To"] = Header(self.main_conf['to'], 'utf-8')
            message["Subject"] = Header('hdc cmd run error', 'utf-8')
        else :
            message = MIMEText('blocks locked at %s' % blocks, 'plain', 'utf-8')
            message["From"] = Header(self.main_conf['user'], 'utf-8')
            message["To"] = Header(self.main_conf['to'], 'utf-8')
            message["Subject"] = Header('blocks locked', 'utf-8')

        return message.as_string()
