# ===================================================================
#
# This script enables HardwareAcceleration.
#
# This script expects the following arguments:
#
# 1. wls.user  (weblogic)
# 2. wls.password  ()
# 3. wls.url (t3://localhost:7001)
# 4. HardwareAcceleration value (true|false)
# ===================================================================

import sys
import os

# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 < 4:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.sh configure_oneflag.py WLS_USER WLS_PASSWORD WLS_URL true"
    exit()

WLS_USER = sys.argv[1]
WLS_PW = sys.argv[2]
WLS_URL = sys.argv[3]
newvalue = sys.argv[4]

print 'Connecting to '+ WLS_URL + ' as user: ' + WLS_USER + ' ...'

# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_URL);

print 'Connecting to Domain ...'
domainCustom()
cd ('oracle.biee.admin')
cd ('oracle.biee.admin:type=BIDomain,group=Service')

print 'Locking the configuration...'
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('lock', objs, strs)

print 'Enabling the HardwareAcceleration...' + newvalue
try:
  if newvalue.lower().find('true') != -1:
    set('HardwareAcceleration', int(true))
  else:
    set('HardwareAcceleration', int(false))
except:
  print "Error::", sys.exc_info()[0]
  objs = jarray.array([], java.lang.Object)
  strs = jarray.array([], java.lang.String)
  invoke('rollback', objs, strs)
  raise

print "Calling commit ..."
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)
print 'Committed OK'

exit()
