# export-retool-log
automation for exporting retool log 


## Overview
Getting logging data from your retool project that placed on retool cloud

- Get project access info
- Enter the Time range of retool logging
- Export as JSON file


## Procedure

### Get ready to run
1. project name: project
2. access token: located in the cookie, when login 
3. xsrf token:   located in the cookie, when login


### 1. Enter project info in main.py

```
PROJECT_NAME = ""
ACCESS_TOKEN = ""
XSRF_TOKEN = ""
```

## 2. Run main.py

```
PROJECT_NAME = ""
ACCESS_TOKEN = ""
XSRF_TOKEN = ""
```


## 3. Enter the date range for retool log

```
enter start date by yyyy.mm.dd:
enter end date by yyyy.mm.dd:
```


## ETC

basically, interval is set into 1 day
change `d` when logging exceeds its limit 

