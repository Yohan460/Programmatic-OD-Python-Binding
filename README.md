# Programmatic OpenDirectory Python Binding
Writing binding information programmatically on macOS Catalina and above

## The Problem
In macOS Catalina the `/Library/Preferences/OpenDirectory/Configurations` folder appears to be protected by SIP or some other unknown protection mechanism. This leaves the common Open Directory binding installation of placing down the configuration plist files nonfunctional. This can be a hard stop when it comes to fully programmatically provisioning a machine via DEP, with the only workaround before discovering this method being using the Directory Utility GUI to manually enter the binding settings.

## The Components of an OD Bind
In a typical Open Directory bind there are three main plist files contained within the Configurations directory, they are as follows:
 
 * `LDAPv3/ldap.domain.contoso.com.plist`
 * `Search.plist`
 * `Contacts.plist`
 
 When analyzing which of these files are actually used for, the `Configurations/ldap.domain.contoso.com.plist` defines the Open Directory server and contains the actual binding information. The `Search.plist` defines the macOS user search space and hierarchies when an Open Directory user attempts to login to the device. Without the `Search.plist`, while a machine may be bound in the technical sense, it will not let a user login. Lastly there is the `Contacts.plist`. This as far as I can tell helps network user contact population and therefore isn't needed. 

## Implementation
1. To write the `ldap.domain.contoso.corp.plist` you have to use the [LDAPv3Write.py](https://github.com/Yohan460/Programmatic-OD-Python-Binding/blob/master/LDAPv3Write.py) script and execute it as follows:

`python /path/to/LDAPv3Write.py /path/to/ldap.domain.contoso.com.plist`

2. To edit default `Search.plist` and append your OpenDirectory bind you run the following command:

`dscl -q localhost -merge /Search CSPSearchPath /LDAPv3/ldap.domain.contoso.com`

3. Add your OD/LDAP Authenticating user to the System keychain using the security command demonstrated below. This username must link to the authenticating user defined within your `ldap.domain.contoso.com.plist`:

`security add-generic-password -a 'USERNAME' -s '/LDAPv3/USERNAME' -w 'pA$$WuRD' -A -T '' /Library/Keychains/System.keychain`

4. Reboot the machine

## Will it continue working?
Your guess is as good as mine

I would recommend using the time the workflow has saved you into migrating to an identity provider that can be bound to using the `dsconfigad` or `dsconfigldap` binaries. If possible removing the binding in it's entirety. I'd recommend looking at [NoMAD Login](https://gitlab.com/orchardandgrove-oss/NoMADLogin-AD) as a viable replacement option as long as there is the capacity to stand up an Active Directory DC.

## Will Apple fix this?
**For them to fix it you as an admin need to file feedback with them that this is an important workflow for you**. 

I will direct you to this [email thread from 2009](https://lists.apple.com/archives/darwin-dev/2009/Feb/msg00127.html) which spells out how `dsconfigldap` does not contain the capability to take in custom ldap attribute mappings.

## How it works
![Shia](https://media.giphy.com/media/ujUdrdpX7Ok5W/giphy.gif)

## Credit
I did not write this script. It was given to me with someone with very in depth knowledge of Apple Devices, but I was given approval to share it out.
