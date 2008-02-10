#!/usr/bin/env python

"""
This parses for NNTP auth commands
and replaces login/pass by another
if user rights are ok.
"""

import pluginbase

######
# CONF #
######

## user list to accept for rewriting
userlist = { "someuser":"somepass",
                    "someotheruser":"someotherpass" }

## real nntp user/pass to submit to the server
realuser = "myaccount"
realpass = "secretpassword"


######
# PROG #
######

class Plugin(pluginbase.PluginBase):
    state = 0

    def filtercall(self, data, inout):
        if inout == "in" : return data ## we filter outgoing only
        if self.state >= 2 : return data ## we already authentificated
        if self.state == 0 :
            begin = data.find("AUTHINFO USER")
            if begin < 0 : return data
            end = data.find("\r\n") 
            self.user = data[begin+len("AUTHINFO USER"):end]
            self.state=1
            if userlist.has_key(self.user.strip()) :
                part1= data[:begin+len("AUTHINFO USER")]
                part2 = data[end - len(data):]
                data = part1 + " " + realuser + " " + part2
                return data
        if self.state == 1:
            begin = data.find("AUTHINFO PASS")
            if begin < 0 : return data
            end = data.find("\r\n")
            self.password = data[begin+len("AUTHINFO PASS"):end]
            self.state=2
            if userlist[self.user.strip()] == self.password.strip() :
                part1= data[:begin+len("AUTHINFO PASS")]
                part2 = data[end - len(data):]
                data = part1 + " " + realpass + " " + part2
            return data
        return data

