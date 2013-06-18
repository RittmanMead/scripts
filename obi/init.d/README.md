# init.d script for OBIEE

Use this script to install OBIEE as a 'service' on Linux, enabling it to be brought up automagically on bootup

## Installation

1. Create this file at `/etc/init.d/obi`, modifying where appropriate the values for : 
	* `SUBSYS` - *This is a freeform name, to identify this environment uniquely. Used in logfile names.*
	* `FMW_HOME` - *The FMW Home folder, eg `/u01/app/oracle/product/fmw`*
	* `ORACLE_OWNR` - *The OS owner under which OBIEE should be managed*
	* `LOGPATH - *Folder in which to store log files - change if you don't want them in `/var/log`*

2. Make it executable

		chmod 750 /etc/init.d/obi
3. Install it as a service

		chkconfig --add obi

## Syntax
	service obi <start|stop|restart|status>

### Manual stop / start

#### Stop

	service obi stop

#### Start

	service obi start

#### Restart

	service obi restart

### OBI Status

	[root@rnm-exa-01 ~]# service obi-dit status
	********************************************************************************
	Oracle BIEE components status....
	********************************************************************************

	 Checking WLS Admin Server...

			WLS Admin Server is running and listening on port 7001

				http://rnm-exa-01:7001/console
				http://rnm-exa-01:7001/em


	 Checking WLS Managed Server (bi_server1) ...

			WLS Managed Server bi_server1 is running and listening on port 9704

				http://rnm-exa-01:9704/analytics


	 Checking OPMN...


	Processes in Instance: instance1
	---------------------------------+--------------------+---------+---------
	ias-component                    | process-type       |     pid | status
	---------------------------------+--------------------+---------+---------
	essbasestudio1                   | EssbaseStudio      |   10486 | Alive
	essbaseserver1                   | Essbase            |    8732 | Alive
	coreapplication_obiccs1          | OracleBIClusterCo~ |    8324 | Alive
	coreapplication_obisch1          | OracleBIScheduler~ |    8325 | Alive
	coreapplication_obijh1           | OracleBIJavaHostC~ |    8322 | Alive
	coreapplication_obips1           | OracleBIPresentat~ |    8321 | Alive
	coreapplication_obis1            | OracleBIServerCom~ |    8323 | Alive

## TODO

Doesn't work for scaled-out deployments yet
