# ===================================================================#
# RNM 2012-11-26
# Add users to WLS LDAP directory, and add them into groups
#
# This script expects the following arguments:
#
# 1. wls.user  (weblogic)
# 2. wls.password  ()
# 3. wls.url (t3://localhost:7001)
# 4. base ID for users
# 5. Password to use for new users
# 6. Group to assign to the users
# 7. Number of users to create
#
# example usage:
# $ /u01/app/oracle/product/fmw3/oracle_common/common/bin/wlst.sh ./add_users.py weblogic Germanbight03 t3://localhost:7004 TestUser UuJ6Il9JeOd0 BIConsumers 50
# ===================================================================

import sys
import os
# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 < 7:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.sh add_users.py WLS_USER WLS_PASSWORD WLS_URL BASE_NAME PW_TO_ASSIGN GROUP NUMBER_OF_USERS"
    exit()

WLS_USER = sys.argv[1]
WLS_PW = sys.argv[2]
WLS_URL = sys.argv[3]
basename = sys.argv[4]
pw = sys.argv[5]
group = sys.argv[6]
numberofusers = int(sys.argv[7])

print WLS_USER, WLS_PW, WLS_URL, basename, pw,  group
print 'Connecting to '+ WLS_URL + ' as user: ' + WLS_USER + ' ...'

# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_URL);

print 'Adding users'
try:
	ix=0
	while ix<numberofusers:
		username = '%s%04d' % (basename,ix)
		print username
		atnr=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider('DefaultAuthenticator')
		atnr.createUser(username,pw,'')
		atnr.addMemberToGroup( group, username)
		ix +=1
except:
	print"Error::", sys.exc_info()[0]
	objs = jarray.array([], java.lang.Object)
	strs = jarray.array([], java.lang.String)
	raise

# Exit
disconnect()
exit()
