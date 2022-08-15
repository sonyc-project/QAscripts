# QA/QC Scripting for Sensor Node Deployment
### Home Sensor TTP Deployment: Summer 2022
- Quality checks sensors for deployment automation
- Pulls via [sonycctl API](https://github.com/sonyc-project/sonycctl/tree/main/sonycctl)

## Dependencies
- [sonycctl](https://github.com/sonyc-project/sonycctl/tree/main/sonycctl) -- click link for installation details
- numpy

  ```
  python -m pip install numpy
  ```


## How to Use
Use ctlscraper.py right before packing the sensor node for shipment to the participant. 

It will prompt you to first log-in to access the sonycctl API. Once credentials are entered, enter a deployment ID to begin. The script will then query sonycctl to pull realtime sensor data.

This script checks 2 aspects:
##### 1) Hardware & Firmware Check
  - Disk Usage
  - WiFi/Cellular Connectivity
  - Mic Connectivity
  - Mic Health
  - Data Uplink
##### 2) Deployment Details Check
  - Deployment Name & ID
  - Deployment Life Stage 


