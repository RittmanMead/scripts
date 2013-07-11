# ===================================================================
# Developed by RNM @ Rittman Mead
# Absolutely no warranty, use at your own risk
# Please include this header in any copy or reuse of the script you make
# ===================================================================#

# Check the status of an Application Deployment# Takes five arguments - connection details, plus application name, and server
# RNM 2012-05-01
import sys
import os
# Check the arguments to this script are as expected.# argv[0] is script name.argLen = len(sys.argv)if argLen -1 < 5:    print "ERROR: got ", argLen -1, " args."    print "USAGE: wlst.sh check_app_state.py WLS_USER WLS_PASSWORD WLS_URL app_name target_server"    exit()WLS_USER = sys.argv[1]WLS_PW = sys.argv[2]
WLS_URL = sys.argv[3]
appname = sys.argv[4]
appserver = sys.argv[5]

print 'Connecting to '+ WLS_URL + ' as user: ' + WLS_USER + ' ...'

# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_URL);

# Set Application run time object
try:
  nav=getMBean('domainRuntime:/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
  state=nav.getCurrentState(appname,appserver)
  print "\033[1;32m " + state + "\033[1;m"
except:
  print "Error::", sys.exc_info()[0]
  objs = jarray.array([], java.lang.Object)
  strs = jarray.array([], java.lang.String)
  raise

disconnect()
exit()
