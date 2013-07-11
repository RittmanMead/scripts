# ===================================================================
# Developed by RNM @ Rittman Mead
# Absolutely no warranty, use at your own risk
# Please include this header in any copy or reuse of the script you make
# ===================================================================#

# Script from Mark R / Venkat
# -----------------------------------------
# Example for enabling or disabling cache
#
# This scripts expects the following arguments:
#
# 1. wls.host (localhost)
# 2. wls.port (7001)
# 3. wls.user  (user1)
# 4. wls.password  (password1)
# 5. newCacheStatus (0=disabled, 1=enabled)

# ===================================================================
import sys
import os

# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 != 5:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.cmd wls_connect.py WLS_HOST WLS_PORT WLS_USER WLS_PASSWORD newCacheStatus"
    print "   eg: wlst.cmd wls_connect.py localhost 7001 user1 password1 1"
    exit()

WLS_HOST = sys.argv[1]
WLS_PORT = sys.argv[2]
WLS_USER = sys.argv[3]
WLS_PW = sys.argv[4]
newCacheStatus = sys.argv[5]

print 'Connecting to '+ WLS_HOST+ ':' + WLS_PORT + ' as user: ' + WLS_USER + ' ...'

# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_HOST+ ':' + WLS_PORT);

print 'Connecting to Domain ...'
domainCustom()
cd ('oracle.biee.admin')
print 'Connecting to BIDomain MBean ...'
cd ('oracle.biee.admin:type=BIDomain,group=Service')

print 'Calling lock ...'
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('lock', objs, strs)

biinstances = get('BIInstances')
biinstance = biinstances[0]

print 'Connecting to BIInstance MBean ...'
cd ('..')
cd (biinstance.toString())

perfconfigbean = get('PerformanceConfiguration')
print 'Connecting to BIInstance Performance Config MBean ...'
cd ('..')
cd (perfconfigbean.toString())
currentCacheStatus=get('BIServerCacheEnabled')
print 'Current Cache Status = ' + str(currentCacheStatus)

print 'Now updating to new setting...'
set('BIServerCacheEnabled',int(newCacheStatus))
currentCacheStatus=get('BIServerCacheEnabled')
print 'New Cache Status = ' + str(currentCacheStatus)

print 'Calling commit ...'
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)

print 'Committed OK'

exit()
