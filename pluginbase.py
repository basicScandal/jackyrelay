#!/usr/bin/env python


"""
This defines the base class for plugins.
"""


class PluginBase:
    def __init__(self, ip):
        self.ip = ip
    def shutdown(self):
        return True
    def filtercall(self, data, inout):
        return data
    def whoami(self):
        return "Not implemented ... whoami() call"


