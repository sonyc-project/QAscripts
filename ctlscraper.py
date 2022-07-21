import sys
# adding sonycctl to system path
sys.path.insert(0, '~/Documents/sonyc/sonycctl')
import sonycctl
import pprint
pp = pprint.PrettyPrinter(indent=4)

"""
|| choosing sensor
    - will want to be able to use fqdn instead of deployment_id
"""
deploy_id = 'deploy-rd4arw' #Input()

"""
|| tapping into sonycctl API
"""
api = sonycctl.API()
api.login()

"""
|| checking status of sensor 
    - is mic connected? DONE
    - is cell hat connected? (is there ppp0/cell_connected=True?)
    - is there an IP address?
    - is signal strength good? (above 85%?)
    - are disk levels good? (tmp_usage, root_usage, varlog_usage) DONE
    - is laeq within range? (~50-60dB) DONE

"""
def sensorCheck(deployment_id):
    status = api.status(deployment_id, start='now-30s')
    s = status[-1]
    # print(s)

    #--CHECK DISK LEVELS:
    diskVariables = ['tmp_usage','root_usage','varlog_usage']
    diskLevels = {key: s[key] for key in s.keys() if key in diskVariables}
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

    #--CHECK MIC CONNECTIVITY:
    if s['mic_connected'] == 1:
        print('GOOD || Mic: connected')
    else:
        print(f"mic bad {s['mic_connected']}")

    #--CHECK LAEQ LEVELS:
    if s['laeq'] > 45 and s['laeq'] < 60:
        print(f"GOOD || LAeq levels -  {s['laeq']}")
    else:
        print(f"Error: laeq levels out of bounds - {s['laeq']}")

sensorCheck(deploy_id)

"""
|| checking SPL levels specifically
    - (optional) check whether SPL levels are within range (could also do this with api.status or api.deploy.info)
"""
spl = api.spl(deploy_id,start = 'now-1m')
# pp.pprint(len(spl))

"""
|| checking deployment info
    - is there a title?
    - is life_stage active?
"""
def deploymentCheck(deployment_id):
    dd = api.deploy.info(deployment_id) #deployment data
    targets = ['title', 'deployment_id', 'life_stage', 'fqdn'] #can get rid of fqdn once fqdn replaces deployment_id
    result = {key: dd[key] for key in dd.keys() if key in targets}
    # pp.pprint(result)
    noValues = [i for i in result if not result[i]]
    # print(noValues)
    if not noValues:
        print('Success: Deployment info looks good')
    else:
        for error in noValues:
            print(f'ERROR: no value for - {error}')
            # raise KeyError(f'ERROR: no value for - {error}')

# deploymentCheck(deploy_id)

"""
|| check audio data
"""
# api.fs('audio', deploy_id)


# for data in api.fs('audio', deploy_id, start='now-5m', end='now'):
#     print(data['id'])
#     api.f(data['id'])
    
# # sonycctl fs ml deploy-qwywf8 --start "2022-06-26T13:00:00" --end "2022-06-26T15:00:00"

# # sonycctl deploy info $DEPLOYID 


