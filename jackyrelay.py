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
import threading
from threading import Thread
from datetime import datetime


from conf.main import *


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
        #self.plugins = []
        #for plugin in activeplugins:
        #    newplugin = plugin.Plugin(self.cip)
        #    self.plugins.append(newplugin)

    
    def filter(self, data,inout):
        if DEBUG : print "prefitler data for %s : %s" % ("in", data)
        for plugin in self.ld.plugins:
            if DEBUG : print "Applying %s plugin filter" % plugin.whoami()
            data = plugin.filtercall(data,inout)
            if DEBUG : print "postfitler data for %s after %s filter: %s" % ("in", plugin.whoami(), data)
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

        self.ld = threading.local()
        self.ld.plugins = []
        for plugin in activeplugins:
            newplugin = plugin.Plugin(self.cip)
            self.ld.plugins.append(newplugin)

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
                        self.shutmedown("hardlink dropped by client on recv")
                    if data : 
                        data = self.filter(data, "out")
                        try:
                            self.c.sendall(data)
                        except :
                            self.shutmedown("hardlink dropped by server on sendall")
                    else : self.shutmedown("Closed by client")
                if sock == self.c:
                    try :
                        data = sock.recv(sbufsize)
                    except :
                        self.shutmedown("hardlink dropped by server on recv")
                    if data : 
                        data = self.filter(data, "in")
                        try :
                            self.s.sendall(data)
                        except :
                            self.shutmedown("hardlink dropped by client on sendall")
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
        
        
        
        
        
