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
DIRECTON = BOTH # Can be : [ "OUTONLY", "INONLY", "BOTH" ]



########
# PROG #
########

class Plugin(pluginbase.PluginBase):
    
    def filtercall(self, data, inout):
        if inout == "in" : 
            if DIRECTION == "OUTONLY" : return data # conf says do not decompress
            # Incomeing data : uncompress it.
            try :
                data = bz2.decompress(data)
            except :
                # not a bzip2 compressed stream
		print "WARNING : TRYED TO DECOMPRESS NOT COMPRESSED DATA, CHECK DIRECTION CONF VALUE"
            return bz2.decompress(data)
        else :
            if DIRECTION == "INONLY" : return data # conf says do not compress
            # Outgoing data : compress it.
            return bz2.compress(data, COMPRESS_LEVEL)









