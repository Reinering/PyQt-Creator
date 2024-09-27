#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""







class Pipreqs:

    PIPREQS_PARAMS = {
        "ignore": ["build", "dist"],   # ignore paths
        "encoding": "utf-8",  # source code encoding
        "force": True,  # force update
        "debug": False,  # print debug info
        "savepath": None,  # save the list of dependencies to a file
    }


    def getCMD(self):
        cmd = ''

        if self.PIPREQS_PARAMS['ignore']:
            cmd = cmd + ' --ignore ' + ','.join(self.PIPREQS_PARAMS['ignore'])

        if self.PIPREQS_PARAMS['encoding']:
            cmd = cmd + ' --encoding ' + self.PIPREQS_PARAMS['encoding']

        if self.PIPREQS_PARAMS['force']:
            cmd = cmd + ' --force'

        if self.PIPREQS_PARAMS['debug']:
            cmd = cmd + ' --debug'

        if self.PIPREQS_PARAMS['savepath']:
            cmd = cmd + ' --savepath ' + self.PIPREQS_PARAMS['savepath']


        return cmd