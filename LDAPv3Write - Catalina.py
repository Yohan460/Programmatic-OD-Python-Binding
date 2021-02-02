#!/usr/bin/python

from OpenDirectory import ODSession, ODNode, kODNodeTypeConfigure
from Foundation import NSData, NSMutableData
import sys

# Reading the LDAP plist
LDAPCONFIGFILE = open(sys.argv[1], "r")
LDAPCONFIG = LDAPCONFIGFILE.read()
LDAPCONFIGFILE.close()

# Write the plist
session = ODSession.defaultSession()
odconfnode, err = ODNode.nodeWithSession_type_error_(session, kODNodeTypeConfigure, None)
config_data = NSData.dataWithBytes_length_(LDAPCONFIG, len(LDAPCONFIG))
root_auth = b'\x00'*32
request = NSMutableData.dataWithBytes_length_(root_auth, 32)
request.appendData_(config_data)
response, err = odconfnode.customCall_sendData_error_(99991, request, None)
