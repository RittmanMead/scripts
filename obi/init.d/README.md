# init.d script for OBIEE

Use this script to install OBIEE as a 'service' on Linux, enabling it to be brought up automagically on bootup, and shutdown when the machine shuts down.

## Installation

1. Create this file at `/etc/init.d/obiee`, modifying where appropriate the values for : 
	* `SUBSYS` - *This must match the filename you create this script as in `/etc/init.d/`*
	* `FMW_HOME` - *The FMW Home folder, eg `/u01/app/oracle/product/fmw`*
	* `ORACLE_OWNR` - *The OS owner under which OBIEE should be managed*
	* `LOGPATH` - *Folder in which to store log files - change if you don't want them in `/var/log`*

	You may also want to change `LSOF_PATH` if the binary is not at `/usr/sbin/lsof` - check using `whereis lsof`

2. Make it executable

		chmod 750 /etc/init.d/obiee

3. Install it as a service

		chkconfig --add obiee

## Syntax
	service obiee <start|stop|restart|status>

### OBI Status

	$ service obiee status

	 Checking WLS Admin Server: listening on port 7001         [  OK  ]
	 Checking WLS Node Manager: listening on port 9556         [  OK  ]
	 Checking WLS Managed Server: listening on port 8205 9704  [  OK  ]
	 Checking OPMN: listening on port 9500 9501                [  OK  ]
		All OPMN-managed BI Components are running         [  OK  ]

### Start

	$ service obiee start

	Starting OBI Admin Server .......                          [  OK  ]
	Starting OBI Node Manager .                                [  OK  ]
	Starting OBI Managed Server.........                       [  OK  ]
	Initiating OBI OPMN startup .                              [  OK  ]

Each component has a timeout associated with it, after which the start process will fail. Change the appropriate `_START_TIMEOUT` values in the script if you want it to wait longer.

### Stop

	$ service obiee stop

	Shutting down OPMN and BI Components.                      [  OK  ]
	Shutting down OBI Managed Server.                          [  OK  ]
	Shutting down OBI Node Manager..                           [  OK  ]
	Shutting down OBI Admin Server.                            [  OK  ]

Each component has a timeout associated with it, after which the process will be forceably killed. Change the appropriate `_STOP_TIMEOUT` values in the script if you want it to wait longer.

### Restart

	$ service obiee restart

	Shutting down OPMN and BI Components.                      [  OK  ]
	Shutting down OBI Managed Server.                          [  OK  ]
	Shutting down OBI Node Manager..                           [  OK  ]
	Shutting down OBI Admin Server.                            [  OK  ]

	Starting OBI Admin Server .......                          [  OK  ]
	Starting OBI Node Manager .                                [  OK  ]
	Starting OBI Managed Server.........                       [  OK  ]
	Initiating OBI OPMN startup .                              [  OK  ]

## Bonus

Use the `watch` command to keep an eye on the status of the service, perhaps whilst it's starting up to see when it's ready: 

	watch service obiee status


## TODO / Known Issues

* Need to parse config.xml to get listen port for managed server, because the Essbase 8205 is really confusing things
* Not set up for scaled-out deployments yet, or AdminServer on a separate host
* If managed server stats in ADMIN mode, it still listens on the port but with no apps running
	* ? Add WLST to check for mngd server status, app deployment status (or is this over-egging it?)
	* ? Add WGET to check that analytics page is up?
