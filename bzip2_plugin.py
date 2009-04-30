#!/usr/bin/env python

"""
This parses for NNTP auth commands
and replaces login/pass by another
if user rights are ok.
"""

import pluginbase

import bz2

########
# CONF #
########

## Compression level 1 to 9.  9 is best compression.
COMPRESS_LEVEL = 9

## Set what to do for each direction :
## Can be : [ "COMPRESS", "DECOMPRESS", None ]
OUT = "COMPRESS"
IN = "DECOMPRESS"



########
# PROG #
########

class Plugin(pluginbase.PluginBase):
    
    def filtercall(self, data, inout):
        if inout == "in" : 
            if IN == "DECOMPRESS" :
                try :
                    data = bz2.decompress(data)
                except :
                    # not a bzip2 compressed stream
            		print "WARNING : TRYED TO DECOMPRESS NOT COMPRESSED DATA, CHECK CONF"
                return bz2.decompress(data)
            if IN == "COMPRESS" :
                return bz2.compress(data, COMPRESS_LEVEL)
        if inout == "out" :
            if OUT == "DECOMPRESS" :
                try :
                    data = bz2.decompress(data)
                except :
                    # not a bzip2 compressed stream
            		print "WARNING : TRYED TO DECOMPRESS NOT COMPRESSED DATA, CHECK CONF"
                return bz2.decompress(data)
            if OUT == "COMPRESS" :
                return bz2.compress(data, COMPRESS_LEVEL)










