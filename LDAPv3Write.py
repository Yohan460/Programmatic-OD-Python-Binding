#!/usr/bin/python

from Foundation import NSBundle, NSData, NSMutableData
OpenDirectory = NSBundle.bundleWithPath_("/System/Library/Frameworks/OpenDirectory.framework")
ODSession = OpenDirectory.classNamed_("ODSession")
ODNode = OpenDirectory.classNamed_("ODNode")
kODNodeTypeConfigure = 8706
import sys

# Reading the LDAP plist
LDAPCONFIGFILE = open(sys.argv[1], "r")
LDAPCONFIG = LDAPCONFIGFILE.read()
LDAPCONFIGFILE.close()

# Write the plist
session = ODSession.defaultSession()
odconfnode = ODNode.nodeWithSession_type_error_(session, kODNodeTypeConfigure, None)
config_data = NSData.dataWithBytes_length_(LDAPCONFIG, len(LDAPCONFIG))
root_auth = b'\x00'*32
request = NSMutableData.dataWithBytes_length_(root_auth, 32)
request.appendData_(config_data)
response = odconfnode.customCall_sendData_error_(99991, request, None)