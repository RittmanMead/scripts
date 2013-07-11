# ===================================================================
# Developed by RNM @ Rittman Mead
# Absolutely no warranty, use at your own risk
# Please include this header in any copy or reuse of the script you make
# ===================================================================#

# Based on Script from Mark R / Venkat, hacked together with John M's script
# -----------------------------------------
# Deploy GCBC webcat  
#
# 1. wls.host (localhost)
# 2. wls.port (7001)
# 3. wls.user  (user1)
# 4. wls.password  (password1)

# ===================================================================
import sys
import os

# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 != 5:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.cmd wls_connect.py WLS_HOST WLS_PORT WLS_USER WLS_PASSWORD WEBCAT_PATH"
    print "   eg: wlst.cmd wls_connect.py localhost 7001 user1 password1 c:\webcat"
    exit()

WLS_HOST = sys.argv[1]
WLS_PORT = sys.argv[2]
WLS_USER = sys.argv[3]
WLS_PW = sys.argv[4]
webcatloc = sys.argv[5]

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
cd('..')


# Go to the presentation server catalog location
cd('oracle.biee.admin:type=BIDomain.BIInstance.PresentationServerConfiguration,biInstance=coreapplication,group=Service')

# Get the old WebCatalogSharedLocation
WebCatalogSharedLocation = get('WebCatalogSharedLocation')
print 'old WebCatalogSharedLocation = ' + WebCatalogSharedLocation 

# set the old WebCatalogSharedLocation
newWebCatalogSharedLocation = webcatloc
set('WebCatalogSharedLocation',newWebCatalogSharedLocation)
WebCatalogSharedLocation = get('WebCatalogSharedLocation')
print 'new WebCatalogSharedLocation = ' + WebCatalogSharedLocation 

print 'Calling commit ...'
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)

print 'Committed OK'

exit()
