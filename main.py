#!/bin/env python3
import config as _ # load config
import json
import requests

def Projects():
    # Get Gitlab Projects
    try:
        URL_RESPONSE = requests.get(_.GITLAB_URL + '/api/v4/projects?private_token=' + _.PRIVATE_TOKEN)
        GITLAB_PROJECTS = json.loads(URL_RESPONSE.text)
    except requests.ConnectionError:
        GITLAB_PROJECTS = []
        print('Connection Error')
        exit()
    # Check Projects
    if GITLAB_PROJECTS != []:
        print('\nList Of Projects to Config: \n')
        for x in range(len(GITLAB_PROJECTS)):
            print([GITLAB_PROJECTS[x]['id'], GITLAB_PROJECTS[x]['name_with_namespace']])
    else:
        print('Notfing to Config')
        exit()

    # Config Gitlab Projects
    START = input('\nType "yes" to continue: ')
    if START == 'yes':
        try:
            for y in range(len(GITLAB_PROJECTS)):
                URL_RESPONSE = requests.put(_.GITLAB_URL + '/api/v4/projects/' + str(GITLAB_PROJECTS[y]['id']),
                    json = {'container_expiration_policy_attributes': _.CLEANUP_POLICY},
                    headers = {'Content-Type': 'application/json;charset=UTF-8', 'PRIVATE-TOKEN': _.PRIVATE_TOKEN}
                )
                if URL_RESPONSE.status_code == 200:
                    print('OK cleanUpPolicy for Project ' + str(GITLAB_PROJECTS[y]['id']) + ' (' + GITLAB_PROJECTS[y]['name_with_namespace'] + ')')
                else:
                    print('ERR cleanUpPolicy for Project ' + str(GITLAB_PROJECTS[y]['id']) + ' (' + GITLAB_PROJECTS[y]['name_with_namespace'] + ')')
        except requests.ConnectionError:
            print('Connection Error')
            exit()

if __name__ == '__main__':
    Projects()
