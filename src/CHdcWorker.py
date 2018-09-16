#!/usr/bin/env python2
#-*- coding: utf8 -*-

import time
import subprocess
import shlex
import json
import logging

from CHdcSession import CHdcSession
import HdcConst

class CHdcWorker :

    def __init__(self, prog_conf):
        self.prog_conf = prog_conf
        self.detect_conf = self.prog_conf['detect']
        self.data = {
            'last_cmd_tt': None,
            'last_cmd_run': None,
            'last_blocks': None
        }

        self.dhc_sess = CHdcSession(prog_conf)
        self.logger = logging.getLogger()

    def start(self):

        while True:
            self._work_per_cycle()
            time.sleep(3)
    
    def _get_health_status_by_cmd(self):       #return (cmd_status, block)
        cmd = self.detect_conf['cmd']
        cmd = shlex.split(cmd)
        output = ''

        try:
            output = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e :
            return (HdcConst.CMD_RUN_ERR, None)
        
        cmd_ret = json.loads(output)
        if 'blocks' in cmd_ret :
            return (HdcConst.CMD_RUN_OVER, cmd_ret['blocks'])
        else :
            return (HdcConst.CMD_RUN_ERR, None)

    def _work_per_cycle(self):
        
        last_cmd_tt = self.data['last_cmd_tt']
        cur_cmd_tt = time.time()

        if (last_cmd_tt == None or 
            abs(cur_cmd_tt - last_cmd_tt) > self.detect_conf['cmd_interval']) :
            (cmd_run, blocks) = self._get_health_status_by_cmd()
            self.data['last_cmd_tt'] = cur_cmd_tt
            self.data['last_cmd_run'] = cmd_run
            self.data['last_blocks'] = blocks

            ret = self.dhc_sess.feed(cur_cmd_tt, cmd_run, blocks)
            self.logger.debug("cur_cmd_tt = %s, cmd_run = %s, blocks = %s, ret = %s" %
                (cur_cmd_tt, cmd_run, blocks, ret)
            )

        else :
            return
