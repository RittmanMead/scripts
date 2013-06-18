# ===================================================================#
# RNM 2012-03-16
# Deploy RPD and restart BI Server
# Cobbled together from scripts by John M, Mark R and Venkat J
#
# Call this script as a parameter to wlst, for example: 
#   %FMW_HOME%/oracle_common/common/bin/wlst.cmd deploy_rpd.py weblogic welcome1 t3://localhost:7001 C:\RPD_to_deploy.rpd Admin123 True
# 
#    This will deploy C:\RPD_to_deploy.rpd with RPD password Admin123. 
#    The weblogic admin server is at t3://localhost:7001/ with credentials weblogic/welcome1
#    The final parameter (0 or 1) indicates whether to restart the BI Server process as part of this script
#       (The RPD won't be active until the BI Server is restarted)
# 
# This script expects the following arguments:
#
# 1. wls.user  (weblogic)
# 2. wls.password  ()
# 3. wls.url (t3://localhost:7001)
# 4. RPD path 
# 5. RPD password
# 6. Restart BI after deploy (True|False)
# ===================================================================

import sys
import os
# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 < 6:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.sh deploy_rpd.py WLS_USER WLS_PASSWORD WLS_URL RPD_PATH RPD_PWD RESTART_BI"
    exit()
else:
	WLS_USER = sys.argv[1]
	WLS_PW = sys.argv[2]
	WLS_URL = sys.argv[3]
	rpdpath = sys.argv[4]
	rpdpass = sys.argv[5]
	restartBI = sys.argv[6]

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

# Deploy RPD
print'Connecting to BIInstance MBean ...'
cd ('..')
cd ('oracle.biee.admin:type=BIDomain.BIInstance.ServerConfiguration,biInstance=coreapplication,group=Service')
print 'Uploading RPD'
try:
	# Set the parameters
	params =  jarray.array([rpdpath,rpdpass],java.lang.Object)
	# Set the parameters Signs
	sign =  jarray.array(['java.lang.String', 'java.lang.String'],java.lang.String)
	# Invoke the procedure
	invoke( 'uploadRepository', params, sign)
except:
	cd ('..')
	cd ('oracle.biee.admin:type=BIDomain,group=Service')
	print"Error::", sys.exc_info()[0]
	objs = jarray.array([], java.lang.Object)
	strs = jarray.array([], java.lang.String)
	invoke('rollback', objs, strs)
	raise


# Commit changes
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)
print 'Committed OK'

if restartBI == 'True':
	print 'Restarting BI server'
	# Restart BI Server
	cd ('..')
	cd ('oracle.biee.admin:oracleInstance=instance1,type=BIDomain.BIInstanceDeployment.BIComponent,biInstance=coreapplication,process=coreapplication_obis1,group=Service')

	print 'Stopping the BI server'
	params = jarray.array([], java.lang.Object)
	signs = jarray.array([], java.lang.String)
	invoke('stop', params, signs)

	BIServerStatus = get('Status')
	print 'BI ServerStatus : ' +BIServerStatus

	print 'Starting the BI server'
	params = jarray.array([], java.lang.Object)
	signs = jarray.array([], java.lang.String)
	invoke('start', params, signs)

	BIServerStatus = get('Status')
	print 'BI ServerStatus : ' +BIServerStatus
else: 
	print '(Skipped restarting BI Server)'
# Exit
exit() 
