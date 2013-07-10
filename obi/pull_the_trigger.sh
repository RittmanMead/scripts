#!/bin/bash
#
# pull_the_trigger.sh
#
# RNM 2012-05-01
#
# For support training :  Do random nasty things to OBIEE
#

FMW_HOME=/home/oracle/obiee
# 
# FMW_HOME is all you need to set .....
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#  Nothing to see here .....
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#  No peeking !
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#  

DOMAIN_HOME=$FMW_HOME/user_projects/domains/bifoundation_domain
ORACLE_BI_HOME=$FMW_HOME/Oracle_BI1
INSTANCE_HOME=$FMW_HOME/instances/instance1
OPMN_STOP="$INSTANCE_HOME/bin/opmnctl stopproc"
# -----------

shutdownoracle () {
sqlplus / as sysdba <<EOF
shutdown immediate
EOF
}

shutdownbimiddleware () {
$ORACLE_BI_HOME/common/bin/wlst.sh <<EOF
connect('weblogic','welcome1','t3://localhost:7001')
progress=stopApplication('bimiddleware')
EOF
}

# -----------
clear
echo ' ------------------------------------------------------------'
echo '                                                 RNM-20120501'
echo ' '
echo ' '
echo '                      OBIEE : Pull The Trigger! '
echo ' '
echo ' This will randomly break something in your OBIEE system '
echo ' '
echo ' It may cause system instability, data loss, and hair loss '
echo ' '
echo ' ----' 
echo ' Press Ctrl-C now to exit'
echo ' Press Return to continue'
echo ' ----'
echo ' '
read line
# -----------
echo '------' >> /tmp/ptt.log
# -----------
number=`echo $RANDOM % 27 + 1 | bc`
echo $number >> /tmp/ptt.log
	if [ $number -le 3 ]; then
		cmd="$OPMN_STOP process-type=OracleBIServerComponent"
	elif [ $number -le 6 ]; then
		cmd="$OPMN_STOP process-type=OracleBIPresentationServicesComponent"
	elif [ $number -le 9 ]; then
		cmd="$OPMN_STOP process-type=OracleBIClusterControllerComponent"
	elif [ $number -le 12 ]; then
		cmd="$OPMN_STOP process-type=OracleBIJavaHostComponent"
	elif [ $number -eq 13 ]; then
		cmd="$OPMN_STOP process-type=OracleBISchedulerComponent"
	elif [ $number -le 16 ]; then
		cmd="lsnrctl stop"
	elif [ $number -le 19 ]; then
		cmd="shutdownoracle"
	elif [ $number -le 22 ]; then
		cmd="$DOMAIN_HOME/bin/stopWebLogic.sh"
	elif [ $number -le 25 ]; then
		cmd="$DOMAIN_HOME/bin/stopManagedWebLogic.sh bi_server1"
	elif [ $number -le 27 ]; then
		cmd="shutdownbimiddleware"
	else
		cmd="sleep 10"
	fi

# Log what we're going to do
date >> /tmp/ptt.log
echo $cmd >> /tmp/ptt.log

# Pull the trigger!
echo -e '\E[01;31;40m'"Gremlins at work . . . . please wait . . . \033[0m"
$cmd 2>>/tmp/ptt.log 1>&2

# -----------------
echo ' '
echo ' '
echo ' '
echo ' '
echo "Done ! "
echo ' '
echo ' Now check OBIEE and figure out what has broken ... '
echo ' '
echo ' '

