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
    - is mic connected?
    - is cell hat connected? (is there ppp0/cell_connected=True?)
    - is there an IP address?
    - is signal strength good? (above 85%?)
    - are disk levels good? (tmp_usage, root_usage, varlog_usage)

"""
status = api.status(deploy_id, start='now-5s')
# pp.pprint(status)

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
def check_deployment():
    dd = api.deploy.info(deploy_id) #deployment data
    targets = ['title', 'deployment_id', 'life_stage', 'fqdn', 'description', 'floor'] #can get rid of fqdn once fqdn replaces deployment_id
    result = {key: dd[key] for key in dd.keys() if key in targets}
    # pp.pprint(result)
    noValues = [i for i in result if not result[i]]
    print(noValues)
    if not noValues:
        print('Success: Deployment info looks good')
    else:
        for error in noValues:
            print(f'ERROR: no value for - {error}')
            # raise KeyError(f'ERROR: no value for - {error}')

check_deployment()

# for item in result:
#     if not result[item]:
#         raise KeyError(f'ERROR: no value for - {item}')
#     else:
#         print('Deployment looks good! ')

# noValues = []
# for item in deployData:
#     if not deployData[item]:
#         noValues.append(item)
#     # print(f'{item}|| {x[item]}')
#     # print(data.key, data.values)
# pp.pprint(f'OK: no value for {noValues}!')


"""
|| check audio data
"""
# api.fs('audio', deploy_id)


# for data in api.fs('audio', deploy_id, start='now-5m', end='now'):
#     print(data['id'])
#     api.f(data['id'])
    
# # sonycctl fs ml deploy-qwywf8 --start "2022-06-26T13:00:00" --end "2022-06-26T15:00:00"

# # sonycctl deploy info $DEPLOYID 


