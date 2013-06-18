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

## Usage

	service obi <start|stop|restart|status>


## TODO

Doesn't work for scaled-out deployments yet
