#!/usr/bin/env python2
#-*- coding: utf8 -*-

import argparse
from CHdc import CHdc


def main():
    parser = argparse.ArgumentParser(
            description="safe's toolkit series - hdc (Health Detect & Check)",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c', '--conf', nargs='?', type=file, default='conf/safe-tk-hdc.json', help='configure for behaviour')
    prog_args = parser.parse_args()
    print prog_args

    inst_hdc = CHdc(prog_args)
    inst_hdc.start()

if __name__ == '__main__' :
    main()
