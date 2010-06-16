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
            if DEBUG :
                print "Before decompression for %s " % DECOMPRESSFOR
                print data
                try :
                    flatdata = bz2.decompress(data)
                except :
                    print "Tryed to decompress not compressed data " 
                    print data
                    return data
                
                print "After decompresson for %s " % DECOMPRESSFOR
                print flatdata
                return flatdata
            else :
                try :
                    flatdata = bz2.decompress(data)
                except :
                    print "Tryed to decompress not compressed data " 
                    if DEBUG : print data
                    return data
                return flatdata
        else : return data
    
    def whoami(self):
        return "Bzip2 decompressor"











