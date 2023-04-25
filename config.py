GITLAB_URL = 'https://gitlab.com/'
PRIVATE_TOKEN = 'your_token'

# https://gitlab.com/help/user/packages/container_registry/reduce_container_registry_storage#use-the-cleanup-policy-api
CLEANUP_POLICY = {
                    'enabled': 'true', 
                    'cadence': '1d',
                    'keep_n': '',
                    'older_than': '30d',
                    'name_regex': '.*',
                    'name_regex_keep': '(?:v.+|master)'
                }
