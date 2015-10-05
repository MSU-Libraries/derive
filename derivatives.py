#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from ConfigParser import ConfigParser

class Derivatives():

    def __init__(self):
        
        self.config_section = "dirs"
        self.get_configs()

    def run_cmds(self):
        process = 1
        try:
            process = subprocess.check_call(self.cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except Exception as e:
            print e

        finally:
            if process <> 0:
                print process

                
        return process

    def get_configs(self):
        
        config = ConfigParser()
        cwd = os.path.dirname(os.path.abspath(__file__))
        config.read(os.path.join(cwd, "settings.cfg"))
        for name, value in config.items(self.config_section):
            setattr(self, name, value)


    def print_process(self):

        print "===Starting {0}".format(self.name)

    def print_output(self):

        if self.return_code == 0:
            print "====={0} succeeded".format(self.name)
        else:
            print "====={0} failed".format(self.name)  