########
# CONF #
########

## put to True if you want to activate ACLs
#useacl = True
useacl = False # /!\ OPEN RELAY /!\

## You can add ips to restrict access
## a dict with 'ip' : max_connections_per_ip
ACL = {}
# ACL = {'129.43.24.87' : 20, 
#    '24.56.12.190' : 1,
#    '42.53.94.24': 10}

#ACL = { '86.238.72.110' : 4 }


## Where to forward ?
destination_host = ('someserver')
destination_port = (80)
jack_port = (6724)
bindto = '0.0.0.0'

# New feature : timeout
# Sets the maxmimum inactivity period of a tunnel *between packets*.
timeout = 60 # in seconds
#timeout = 300 # set this on slow links

# New freature : receive from server buf size
# buf size between jacky and the server
sbufsize = 650 * 1024 # 650ko
#sbufsize = 64 * 1024 # set this on slow links

# New freature : receive from client buf size
# buf size between you and jacky
cbufsize = 64 * 1024 # 64 ko


###########
# PLUGINS #
###########

## This one basicly logs stuff
import simple_logger_plugin as simple_logger

## This one filters login/pass from nntp authentification
## uses it to check user rights
## and replaces it by other login/pass before forwarding.
import nntp_auth_rewrite_plugin as nntp_auth_rewrite


### This one compresses and uncompresses in bzip2
import bzip2_compressor_plugin as bzip2_compressor
import bzip2_decompressor_plugin as bzip2_decompressor

## ORDER IS IMPORTANT
activeplugins = [] # None activated 
#activeplugins = [ bzip2_decompressor, nntp_auth_rewrite, simple_logger , bzip2_compressor ]
#activeplugins = [ nntp_auth_rewrite , bzip2_compressor ]
#activeplugins = [ bzip2_decompressor, nntp_auth_rewrite ]
