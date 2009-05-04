#!/usr/bin/env python

"""
This simple plugin logs input/output
"""

import pluginbase


class Plugin(pluginbase.PluginBase):
    ## CONF
    infile = "logdata.log"
    outfile = "logdata.log"
    
    def __init__(self, ip):
        self.ip = ip
        self.infile = ip + self.infile
        self.outfile = ip + self.outfile
        ## Open handles right away for speed.
        self.hdl_in = open(self.infile, 'a')
        if self.infile == self.outfile : self.hdl_out = self.hdl_in
        else : self.hdl_out = open(self.outfile, 'a')
    
    def shutdown(self):
        self.hdl_in.close()
        self.hdl_out.close()
        return True
    
    def filtercall(self, data, inout):
        if inout == "in" : self.hdl_in.write(" <--  " + data)
        else : self.hdl_out.write(" -->  " + data)
        return data
    
    def whoami(self):
        return "Simple logger"

