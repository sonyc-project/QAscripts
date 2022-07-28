import sys
sys.path.insert(0, '~/Documents/sonyc/sonycctl') # adding sonycctl to system path
import sonycctl
import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=4)

"""
|| choosing sensor
    - will want to be able to use fqdn instead of deployment_id
"""
deploy_id = 'deploy-rd4arw' #Input("Enter deployment id...")

"""
|| tapping into sonycctl API
"""
api = sonycctl.API()
api.login()

"""
|| checking status of sensor 
    - [DONE] is mic connected? 
    - [DONE] is cell hat connected? (is there ppp0/cell_connected=True?)
    - [DONE] is there an IP address? (wlan0_ip)
    - [DONE] is signal strength good? (cell_strength - above 85%?)
    - [DONE] are disk levels good? (tmp_usage, root_usage, varlog_usage)
    - [DONE] is laeq within range? (~50-60dB)

"""

class SensorHealth:
    def __init__(self, deploymentID):
        self.deploymentID = deploymentID
        deploymentInfo = api.status(self.deploymentID, start='now-30s')
        self.deployStatus = deploymentInfo[-1]
    def checkCellUp(self):
        if self.deployStatus['cell_connected'] and self.deployStatus['ppp0_ip']:
            print(f"GOOD || Cell Hat USB connected & online")
        elif self.deployStatus['cell_connected'] and not self.deployStatus['ppp0_ip']:
            print(f"Error: Cell Hat USB connection detected, but no cell internet connection, is there a sim card?")
        else:
            print(f"Error: Cell Hat USB not connected")

        #-- CHECK CELL_STRENGTH:
        if np.abs(self.deployStatus['cell_strength']) > 85:
            print(f"GOOD || CELL STRENGTH: {np.abs(self.deployStatus['cell_strength'])}%")
        else:
            print(f"Error: Bad cell strength {np.abs(self.deployStatus['cell_strength'])}%")

        # pass
    def checkIP(self):
        if self.deployStatus['wlan0_ip']:
            print(f"GOOD || IP ADDRESS: {self.deployStatus['wlan0_ip']}")
        else:
            print(f"Error: No IP ADDRESS")
        # pass
    def checkDiskUsage(self):
        diskVariables = ['tmp_usage','root_usage','varlog_usage']
        diskLevels = {key: self.deployStatus[key] for key in self.deployStatus.keys() if key in diskVariables}
        # print(diskLevels)
        outBounds = [i for i in diskLevels if diskLevels[i] >=15]
        # print(outBounds)
        if not outBounds:
            print('GOOD || Disk Levels: in bounds')
            for g in diskLevels:
                pp.pprint(f'{g}:{diskLevels[g]}')
        else:
            for x in outBounds:
                print(f'Error: {x} value out of bounds - {diskLevels[x]}')
        # pass
    def checkMicUp(self):
        if self.deployStatus['mic_connected'] == 1:
            print('GOOD || Mic: connected')
        else:
            print(f"mic bad {self.deployStatus['mic_connected']}")

        #-- CHECK LAEQ LEVELS:
        if self.deployStatus['laeq'] > 40 and self.deployStatus['laeq'] < 60:
            print(f"GOOD || LAeq levels -  {self.deployStatus['laeq']}")
        else:
            print(f"Error: laeq levels out of bounds - {self.deployStatus['laeq']}")

        # pass
    def checkAll(self):
        print(f'---------------- Checking all sensor [{self.deploymentID}] statuses... ----------------')
        print("==============\nChecking CELL STATUS...\n==============")
        self.checkCellUp()
        print("==============\nChecking DISK STATUS...\n==============")
        self.checkDiskUsage()
        print("==============\nChecking IP STATUS...\n==============")
        self.checkIP()
        print("==============\nChecking MIC STATUS...\n==============")
        self.checkMicUp()

# testid = SensorHealth(deploy_id) 
# testid.checkAll()


"""
|| [DONE] checking deployment info
    - is there a title?
    - is life_stage active?
"""
class DeploymentHealth:
    def __init__(self, deploymentID):
        self.deploymentID = deploymentID
        targets = ['title', 'deployment_id', 'life_stage', 'fqdn'] #can get rid of fqdn once fqdn replaces deployment_id
        self.dd = api.deploy.info(self.deploymentID)
        self.result = {key: self.dd[key] for key in self.dd.keys() if key in targets}
    def checkValues(self):
        noValues = [i for i in self.result if not self.result[i]]
        if not noValues:
            print('Success: Deployment info looks good')
            pp.pprint(self.result)
        else:
            for error in noValues:
                print(f'ERROR: no value for - {error}')
                # raise KeyError(f'ERROR: no value for - {error}')

testid_deploy = DeploymentHealth(deploy_id) 
testid_deploy.checkValues()

"""
|| check audio data
"""
# api.fs('audio', deploy_id)


# for data in api.fs('audio', deploy_id, start='now-5m', end='now'):
#     print(data['id'])
#     api.f(data['id'])
    
# # sonycctl fs ml deploy-qwywf8 --start "2022-06-26T13:00:00" --end "2022-06-26T15:00:00"

# # sonycctl deploy info $DEPLOYID 


