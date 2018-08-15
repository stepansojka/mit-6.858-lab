#!/usr/bin/python

import rpclib
import sys
import auth
import os
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    def rpc_login(self, username, password):
        return auth.login(username, password)

    def rpc_register(self, username, password):
        return auth.register(username, password)

    def rpc_check_token(self, username, token):
        return auth.check_token(username, token)

(_, dummy_zookld_fd, sockpath) = sys.argv

print >> sys.stderr, 'uid: ', os.getuid()

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
