# Multi-Client Reporting Utility for OpsRamp  

## Purpose

This is a utility intended for use by OpsRamp customers needing to batch-generate some useful reports across all tenants in their partner instance.

## First time execution
The first time it is run, it will look to see if the default environment config directory exists, and if it's not there it will create it.

After that, you can either update the environments.yml file in the environment config directory with your partner-level OpsRamp API credentials, or you can specify API credentials on the command line.

## Available Reports
The following reports are currently available.  Each report generates a separate report file for each tenant unless ptherwise specified:

### Server Utilization Comparison
This report contains a page for each Windows or Linux server in the environment, with time-series graphs for the speficied period for CPU Utilization, File System Utilization, and Memory Utilization.  A table at the bottom of each page shows min, max, and average for the current period and increase/decrease trend from the baseline period.

### Network Utilization
This is a fairly standard Top N report for Cisco device CPU Utilization, Memory Utilization, and Interface Utilization, Errors, etc.  It shows a time series only for the Top N items, followed by a detail report of all items sorted from highest to lowest.

### Patch Management
Summary of patches installed in the reporting period in pdf format


### Remote Control Usage
Histogram and detailed list of remote control console sessions that occurred in the reporting period.

### Hardware Inventory
This provides a list of resources in either excel (default) or pdf format

### Software Inventory
This provides a list of installed applications and services for each device in pdf format


## Command line help:


    usage: opreport [-h] [--env ENV] [--envfile ENVFILE] [--api_url API_URL] [--key KEY] [--secret SECRET] [--tenant TENANT] [--start START] [--end END]
                    [--outdir OUTDIR] [--logo LOGO] [--secure SECURE] [--tenant_criteria TENANT_CRITERIA]
                    {uc,nu,pm,rcu,hi,si} ...

    Multi-Client Reporting Utility for OpsRamp

    positional arguments:
    {uc,nu,pm,rcu,hi}     Available commands
        uc                  Generate Server Utilization Comparison Reports
        nu                  Generate Network Utilization Reports
        pm                  Generate Patch Management Reports
        rcu                 Generate Remote Control Usage Reports
        hi                  Generate Hardware Inventory Reports
        si                  Generate Software Inventory Reports

    optional arguments:
    -h, --help            show this help message and exit
    --start START         Start date of reporting period in YYYY-MM-DD format (default=1st of prior month)
    --end END             End date of reporting period in YYYY-MM-DD format (default=Last day of prior month)
    --outdir OUTDIR       Directory where report output will be written (Default: ./output)
    --logo LOGO           Logo image file for report headers (Default: /Users/michael.friedhoff/Library/Application Support/OpsRamp/logo.jpeg)
    --secure SECURE       Whether or not to verify SSL cert (Default: True)
    --tenant_criteria TENANT_CRITERIA
                            Search criteria for which tenants to include as per https://develop.opsramp.com/tenancy-access-controls/tenants-orgid-
                            clients-search (Default: "activeStatus:true", which will include all active tenants)

    Use yaml environment file credentials:
    --env ENV             Name of environment to use, referencing a named set of API credentials in environments.yml
    --envfile ENVFILE     Location of environments YAML file to be used (Default: /Users/michael.friedhoff/Library/Application
                            Support/OpsRamp/environments.yml)

    Use command line credentials:
    --api_url API_URL     Customer-specific API URL such as https://mycompany.api.opsramp.com
    --key KEY             Authentication key
    --secret SECRET       Authentication secret
    --tenant TENANT       Authentication MSP or Tenant ID