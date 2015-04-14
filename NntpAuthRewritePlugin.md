## Introduction ##

nntp\_auth\_rewrite plugin is a quite cool feature :
  * can extract login / password from nntp authentification
  * can check it against it's own acls
  * if in acls, it can replace submited login/password before submitting to the remote server.


### configuration ###

Open the plugin file : nntp\_auth\_rewrite\_plugin.py


#### option : userlist ####
-is a python dic : { "someuser":"somepass", "someotheruser":"someotherpass" }

-is the plugin's acl list. Any login/pass extracted from the protocol witch matches one of theses will be rewrited

#### option : realuser ####
the user you want to rewrite the matched acls to

#### option : realpass ####
the password you want to rewrite the matched acls to



### Enable Plugin ###

to enable plugin add nntp\_auth\_rewrite to activeplugins option in jackyrelay.py

exemple : ` activeplugins = [ nntp_auth_rewrite ] `

