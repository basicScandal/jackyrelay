#!/usr/bin/env python

## jackrelay
## GPLv2+
## Author : Philippe Mironov <mir@freecontrib.org>

"""
jackrelay is an advanced tcp forwarder.
Multi-threaded multi-client tcp relay :)
ACL by ip capable
plugin based filters support
"""

import time, socket, select
from threading import Thread
from datetime import datetime


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

## ORDER IS IMPORTANT
activeplugins = [] # None activated 
#activeplugins = [ nntp_auth_rewrite, simple_logger ]
#activeplugins = [ nntp_auth_rewrite ]

########
# PROG #
########

#GLOBALS :
connectedips = {}


class Forwarder(Thread):
    '''
    This handles a tunnel.
    '''
    def __init__(self, server, cip):
        Thread.__init__(self)
        self.s = server
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cip = cip
        self.plugins = []
        for plugin in activeplugins:
            newplugin = plugin.Plugin(self.cip)
            self.plugins.append(newplugin)

    
    def filter(self, data,inout):
        for plugin in self.plugins:
            data = plugin.filtercall(data,inout)
        return data
        
    def shutmedown(self, msg = None):
        global connectedips
        if msg: print self.cip, " : ", msg
        connectedips[self.cip] = connectedips[self.cip] -1
        self.s.close()
        self.c.close()
        self.stop = True
        print "Closed ", self.cip

    def run(self):
        global connectedips
        print datetime.now(), " Trying to connect to %s:%s" % (destination_host, destination_port)
        self.c.connect((destination_host, int(destination_port)))
        print datetime.now(), " Jack connected to %s:%s" % (destination_host, destination_port)
        sockets = [ self.s, self.c ]

        self.stop = False
        while not self.stop:
            readysocks, waste1, waste2 = select.select(sockets, [], [], timeout)
            if not len(readysocks) :  # we timeouted
                self.shutmedown("has timeouted")
            for sock in readysocks :
                if sock == self.s:
                    try :
                        data = sock.recv(cbufsize)
                    except :
                        data = ""
                    if data : self.c.sendall(self.filter(data, "out"))
                    else : self.shutmedown("Closed by client")
                if sock == self.c:
                    try :
                        data = sock.recv(sbufsize)
                    except:
                        data = ""
                    if data : self.s.sendall(self.filter(data, "in"))
                    else : self.shutmedown("Closed by server")


def main():
    threadpool = []
    global connectedips
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #addr = (socket.gethostname() , jack_port)
    addr = (bindto, jack_port)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    srv.bind(addr)
    srv.listen(1)
    print datetime.now(), " Listening on %s:%s" % addr
    if useacl : print "Useing ACLs : ", ACL
    else : print "No ACLs /!\ OPEN RELAY MODE /!\ "

    while 1 : #infinit loop
        s, url = srv.accept()
        cip, cport = url
        print "Client connected to Jack from %s" % str(url)
        if useacl :
            if ACL.has_key(cip) : 
                #check nb conneted ips
                if not connectedips.has_key(cip):
                    connectedips[cip] = 0
                    ok = True
                else : 
                    if connectedips[cip] < ACL[cip] : ok = True
                    else :
                        ok = False
                        print datetime.now(), ' %s is already connected %s out of %s max' % (cip, connectedips[cip], ACL[cip])
            else : 
                ok = False
                print datetime.now(), cip, " not in ACL list, rejecting" 
                #print 'ACL list is : ', ACL
        if not useacl :
            if not connectedips.has_key(cip): connectedips[cip] = 0
            ok = True
            
        if ok : 
            t = Forwarder(s, cip)
            threadpool.append(t)
            connectedips[cip] += 1
            t.start()
        else :
            s.close()
                




if __name__ == '__main__':
        ##Profiling
        #import profile
        #profile.run('main()', 'jackyrelay.prof')
        main()
        
        
        
        
        
