# ===================================================================
# Developed by RNM @ Rittman Mead
# Absolutely no warranty, use at your own risk
# Please include this header in any copy or reuse of the script you make
# ===================================================================#

# Based on Script from Mark R / Venkat, hacked together with John M's script
# -----------------------------------------
# Enable Usage Tracking and Summary Advisor Statistics logging
# Assumes that RPD has been updated with database and connection as stated below
#
# RNM 2012-05-04
#
# ===================================================================
import sys
import os

# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 != 3:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst.sh enable_ut_sa.py WLS_USER WLS_PASSWORD WLS_URL"
    print "   eg: wlst.sh enable_ut_sa.py weblogic password t3://localhost:7001"
    exit()

WLS_USER = sys.argv[1]
WLS_PW = sys.argv[2]
WLS_URL = sys.argv[3]

print 'Connecting to '+ WLS_URL + ' as user: ' + WLS_USER + ' ...'

# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_URL);

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


# Go to the BI Server configuration
cd('oracle.biee.admin:type=BIDomain.BIInstance.ServerConfiguration,biInstance=coreapplication,group=Service')

# Update usage tracking configuration
print 'Existing configuration'
print '----------------------'
print get('SummaryAdvisorTableName')
print get('SummaryStatisticsLogging')
print get('UsageTrackingCentrallyManaged')
print get('UsageTrackingConnectionPool')
print get('UsageTrackingDirectInsert')
print get('UsageTrackingEnabled')
print get('UsageTrackingPhysicalTableName')


# Update usage tracking configuration
set('SummaryAdvisorTableName','"FMW Metadata Repository"."DEV_BIPLATFORM"."S_NQ_SUMMARY_ADVISOR"')
set('SummaryStatisticsLogging','YES')
set('UsageTrackingCentrallyManaged',1)
set('UsageTrackingConnectionPool','"FMW Metadata Repository"."RCU Connection Pool"')
set('UsageTrackingDirectInsert',1)
set('UsageTrackingEnabled',1)
set('UsageTrackingPhysicalTableName','"FMW Metadata Repository"."DEV_BIPLATFORM"."S_NQ_ACCT"')

print 'Updated configuration'
print '---------------------'
print get('SummaryAdvisorTableName')
print get('SummaryStatisticsLogging')
print get('UsageTrackingCentrallyManaged')
print get('UsageTrackingConnectionPool')
print get('UsageTrackingDirectInsert')
print get('UsageTrackingEnabled')
print get('UsageTrackingPhysicalTableName')


print 'Calling commit ...'
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)

print 'Committed OK'

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

# Exit
exit()

