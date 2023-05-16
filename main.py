#!/bin/env python3
import config as _ # load config
import json
import requests
import sys

def Projects():
    # Get Gitlab Projects
    GITLAB_PROJECTS = []
    PAGE = 1
    try:
        while True:
            URL_RESPONSE = requests.get(f"{_.GITLAB_URL}/api/v4/projects?private_token={_.PRIVATE_TOKEN}&per_page=100&page={PAGE}")
            GITLAB_PROJECTS += json.loads(URL_RESPONSE.text)
            if len(URL_RESPONSE.json()) == 0: break
            PAGE += 1
    except requests.ConnectionError:
        print('Connection Error')
        exit()
        
    # Check Projects
    if GITLAB_PROJECTS != []:
        print('\nList Of Projects to Config: \n')
        for x in range(len(GITLAB_PROJECTS)):
            for key in _.CLEANUP_POLICY:
                if key in GITLAB_PROJECTS[x]['path_with_namespace']:
                    print([GITLAB_PROJECTS[x]['id'], GITLAB_PROJECTS[x]['path_with_namespace']], f"project will use policy '{key}'")
    else:
        print('Notfing to Config')
        exit()

    # Check Start
    try:
        if sys.argv[1] == '--force':
            START = 'yes'
    except IndexError:
        START = input('\nType "yes" to continue: ')
    
    # Config Gitlab Projects
    try:
        if START == 'yes':
            for x in range(len(GITLAB_PROJECTS)):
                for key in _.CLEANUP_POLICY:
                    if key in GITLAB_PROJECTS[x]['path_with_namespace']:
                        URL_RESPONSE = requests.put(f"{_.GITLAB_URL}/api/v4/projects/{str(GITLAB_PROJECTS[x]['id'])}",
                            json = {'container_expiration_policy_attributes': _.CLEANUP_POLICY[key]},
                            headers = {'Content-Type': 'application/json;charset=UTF-8', 'PRIVATE-TOKEN': _.PRIVATE_TOKEN}
                        )
                        if URL_RESPONSE.status_code == 200:
                            print(f"OK cleanUpPolicy for Project {str(GITLAB_PROJECTS[x]['id'])} ({GITLAB_PROJECTS[x]['path_with_namespace']})")
                        else:
                            print(f"ERR cleanUpPolicy for Project {str(GITLAB_PROJECTS[x]['id'])} ({GITLAB_PROJECTS[x]['path_with_namespace']})")
    except requests.ConnectionError:
        print('Connection Error')
        exit()

if __name__ == '__main__':
    Projects()
