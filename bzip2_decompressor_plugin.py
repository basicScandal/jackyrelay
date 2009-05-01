#!/usr/bin/env python

"""
This filter decompresses from bzip2
"""

import pluginbase

import bz2

from conf.bzip2_decompress import *

########
# PROG #
########

class Plugin(pluginbase.PluginBase):
    
    def filtercall(self, data, inout):
        if inout == DECOMPRESSFOR : 
            try :
                flatdata = bz2.decompress(data)
            except :
                print "Tryed to decompress not compressed data " 
                if DEBUG : print data
                return data
            return flatdata
        else : return data











