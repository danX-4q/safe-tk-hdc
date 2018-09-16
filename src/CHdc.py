#!/usr/bin/env python2
#-*- coding: utf8 -*-

import json
import logging
from logging.handlers import RotatingFileHandler

from CHdcWorker import CHdcWorker
#from CHdcAction import CHdcAction

class CHdc:

    def __init__(self, prog_args):
        self.prog_args = prog_args
        self.logger = None
        self.worker = None

    def start(self):
        self.prog_conf = json.load(self.prog_args.conf)
        self._start_log()

        self.worker = CHdcWorker(self.prog_conf)
        self.worker.start()

    def _start_rotating_log(self, prog_conf_log_rotating):
        
        Rthandler = RotatingFileHandler(
            prog_conf_log_rotating['file'], 
            prog_conf_log_rotating['maxBytes'],
            prog_conf_log_rotating['backupCount'])

        #Rthandler.setLevel(logging.INFO)   #when not set, use default basic config
        formatter = logging.Formatter(prog_conf_log_rotating['formatter'])

        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler)

    def _start_log(self):
        
        log_level_para = {
            "debug": logging.DEBUG,
            "info" : logging.INFO,
            # and others...
        }
        log_level = self.prog_conf['log']['basic']['level']
        log_level = log_level_para[log_level]
        log_datefmt = self.prog_conf['log']['basic']['datefmt']
        logging.basicConfig(level=log_level, format=self.prog_conf['log']['basic']['formatter'], datefmt=log_datefmt)

        rotating_enable = False
        if ('rotating' in self.prog_conf['log'] and 
            self.prog_conf['log']['rotating']['enable']) :
            self._start_rotating_log(self.prog_conf['log']['rotating'])
            rotating_enable = True

        self.logger = logging.getLogger()

        if ('console' in self.prog_conf['log'] and 
            not self.prog_conf['log']['console']['enable']) :
            #disable console log

            if rotating_enable :
                lhStdout = self.logger.handlers[0]
                self.logger.removeHandler(lhStdout)
            else :
                self.logger.warning('disable rotating log, so can not disable console log')
        
        ###
        self.logger.info('start logger successfully')

    #######################################################


