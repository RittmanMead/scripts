This is a set of scripts and response files that you can use for semi-automating the silent install of Exalytics (based on OBI 11.1.1.7 and TT 11.2.2.5). 

It is hacked together, but served its purpose well for me. 

It was designed for use installing multiple environments on the same server, hence the use of static-ports.ini etc.

For details, see https://rittmanmead.zendesk.com/entries/24077092-Exalytics-installation-runbook

1. Run sed -i -e 's/XX_STR_XX/value/g' on all the following: 

		sed -i -e 's/XX_INSTALL_TEMPLATES_XX/value/g'      # Where the installation templates/response files are, such as this one
		sed -i -e 's/XX_HOSTNAME_XX/value/g'               
		sed -i -e 's/XX_FMW_HOME_XX/value/g'
		sed -i -e 's/XX_RCU_CONN_XX/value/g'		  # host:port:sid
		sed -i -e 's/XX_RCU_PREFIX_XX/value/g'
		sed -i -e 's/XX_TT_INSTANCE_XX/value/g'
		sed -i -e 's/XX_RCU_MDS_PW_XX/value/g'
		sed -i -e 's/XX_WLS_ADMIN_PW_XX/value/g'
		sed -i -e 's/XX_RCU_SYSDBA_PW_XX/value/g'
		sed -i -e 's/XX_RCU_BIPLATFORM_PW_XX/value/g'

2. Create static-ports.ini file, use this to increment port numbers by 10000: 

		awk '{if ($NF ~ /[0-9]+/) gsub($NF,($NF)+10000);print}' static-ports.ini

3. Update ports in bim-setup.properties:
	* AdminServer (per static-ports.ini)
	* TT daemon (suggested increment is 1000)
	* TT server (suggested increment is 1000)

4. Execute shell scripts 01 - 05
