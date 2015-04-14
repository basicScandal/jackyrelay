# Documentation #

This page will cover the basic of how-to configure and use jackyrelay and it's filters.
You'll find documentation directly in the configuration files.


## jackyrelay ##



The bare program (without modules) is quite simple.
It basicly establishes **a tunnel between clients** that connect to it and **a remote server**. It has an ACL ip based capability.

### install ###
First get the latest tarball from [this page](http://code.google.com/p/jackyrelay/downloads/list) then simply untar it somewere.

It has no special dependencies. Any version of python from 2.3 should do.

### options ###

Let's look at the option. For that you'll have to open jackyrelay.py file.
The configuration is done directly in that file.

Options are all under **CONF** header.

#### useacl ####
-is a boolean True/False

-triggers the use of the ACLs.
  * If you set it to False, any connection to jackyrelay will be accepted.
  * If you set it to True, any connection not matching the ACLs will be rejected.


#### ACL ####
-is a python dictionnary  { 'key1' : 'value1', 'key2' : 'value2' }

-defines ips and connections per ip restrictions.
  * key is the ip
  * value is the max number of connections for that ip

exemple:
```
ACL = { '86.228.12.10' : 4, '24.56.12.190' : 1 }
```
will accept 4 connections from 86.228.12.10 and 1 from 24.56.12.190


#### destination\_host ####
- is a string.
  * host or ip of the remote server

exemple :
```
destination_host = 'service.someserver.com'
```


#### destination\_port ####
- is a integer
  * port of the remote server

exemple :
```
destination_port = 80 # HTTP
destination_port = 119 # NNTP
```



#### jack\_port ####
- is a integer
  * port jackyrelay will listen on
  * on UNIX systems you will need root rights to use a port under <1024

exemple :
```
jack_port = 9080 # unprevileged port can be run as user
jack_port = 119 # previleged port, you will need to be root
```



#### bindto ####
- is a string.
  * ip to bind to
  * restricts jackyrelay to some ip/interface.
  * '0.0.0.0' if unsure

exemple :
```
bindto = '0.0.0.0' # bind on every interfaces and all avaible ips
bindto = '127.0.0.1' # bind on localhost only
```


## plugins ##

The PLUGIN section in jackyrelay.py contains plugin activation.

Add a plugin to ` activeplugins ` list to enable the plugin filter.

Please note that filters will be chained so the order you add them is important.

Few exemples :

```
activeplugins = [] # None activated
activeplugins = [ nntp_auth_rewrite, simple_logger ] # will rewrite then log
activeplugins = [ nntp_auth_rewrite ] # will rewrite only
activeplugins = [ simple_logger, nntp_auth_rewrite ] # will log then rewrite
```

Each plugin has it's own documentation page :

  * NntpAuthRewritePlugin is an NNTP related filter.