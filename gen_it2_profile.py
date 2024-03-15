import copy
import csv
import json
import os
import sys
import uuid

dynamic_profile = {
    'Profiles': []
}

profile_template = {
    'Name': '',
    'Guid': '',
    'Custom Command': 'Yes',
    'Command': '',
    'Tags': [
        ''
    ]
}

user_name = os.environ.get('USER_NAME', os.environ['USER'])

new_profiles = []
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        new_profiles.append(line)

for profile in new_profiles:
    new_profile = copy.deepcopy(profile_template)
    new_profile.update(profile)
    new_profile['Guid'] = str(uuid.uuid4())
    tags = [tag.strip() for tag in profile['Tags'].split(',')]
    new_profile['Tags'] = tags
    new_profile['Command'] = new_profile['Command'].replace('USER_NAME', user_name)
    dynamic_profile['Profiles'].append(
        new_profile
    )

with open(sys.argv[2], 'w+') as outfile:
    outfile.write(json.dumps(dynamic_profile, indent=2))
