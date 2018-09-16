#!/usr/bin/env python2
#-*- coding: utf8 -*-

import json
import time
import logging

import HdcConst

class CHdcSession :

    def __init__(self, prog_conf):
        self.prog_conf = prog_conf
        self.sess_conf = self.prog_conf['session']
        self.logger = logging.getLogger()

        self.last_cmd_run = None
        self.last_cmd_tt = None
        self.last_blocks = 0

    def feed(self, cur_cmd_tt, cmd_run, blocks) :       #return true(trigger action)

        if self.last_cmd_run == None:
            self.last_cmd_run = cmd_run
            self.last_cmd_tt = cur_cmd_tt
            self.last_blocks = blocks
            return False
        
        if cmd_run == self.last_cmd_run :
            if cmd_run == HdcConst.CMD_RUN_ERR :
                #repeat error
                if abs(cur_cmd_tt - self.last_cmd_tt) > self.sess_conf['err_trigger_interval'] :
                    self.last_cmd_tt = cur_cmd_tt
                    self.last_blocks = blocks
                    self.logger.info('keep repeating cmd_run_err, trigger action')
                    return True
                else :
                    self.last_blocks = blocks
                    return False
            else :
                #repeat over
                if blocks == self.last_blocks :
                    if abs(cur_cmd_tt - self.last_cmd_tt) > self.sess_conf['lock_trigger_interval'] :
                        self.last_cmd_tt = cur_cmd_tt
                        self.logger.info('keep repeating cmd_run_over at blocks, trigger action')
                        return True
                    else :
                        return False
                else :
                    self.last_cmd_tt = cur_cmd_tt
                    self.last_blocks = blocks
                    self.logger.info('cmd_run_over, increating blocks')
                    return False
        else :
            if cmd_run == HdcConst.CMD_RUN_ERR :
                #over -> err
                self.last_cmd_run = cmd_run
                self.last_cmd_tt = cur_cmd_tt
                self.last_blocks = blocks
                self.logger.info('cmd_run_over -> cmd_run_err, do not trigger action at once')
                return False
            else :
                #err -> over
                self.last_cmd_run = cmd_run
                self.last_cmd_tt = cur_cmd_tt
                self.last_blocks = blocks
                self.logger.info('cmd_run_err -> cmd_run_over, do not trigger action at once')
                return False
