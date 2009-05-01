#!/usr/bin/env python

"""
This filter compresses in bzip2
"""

import pluginbase

import bz2

from conf.bzip2_compress import *

########
# PROG #
########

class Plugin(pluginbase.PluginBase):
    
    def filtercall(self, data, inout):
        if inout == COMPRESSFOR : 
            if not data :
                print "something is fucked up : %s" % data
                return data
            return bz2.compress(data, COMPRESS_LEVEL)
        else : return data


