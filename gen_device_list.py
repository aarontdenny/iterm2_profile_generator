# This script will generate xxx.csv file that can be used by gen_xxxxx_prod.sh
# Modify tag_filter to obtain proper tags from hostname

import yaml
import re
import os
import csv

# Set the prefix for profile name. Usually a company name
profile_prefix = 'Company'
regex_tags = r'(^DC1|^DC2).*'

# Load hostvar .yml files. Specify the path to the directory
path = "../../ansible/host_vars/"
filelist = sorted(os.listdir(path))

# Create csv file. Specify the name of the file.
file_name = 'Company_iterm.csv'
profiles = 0

print(f"Creating CSV to be used to create iTerm2 Profiles: {file_name} \n")

with open(file_name, 'w', newline='') as csvfile:
    # Define the header for the csv file
    fields = ['Name', 'Command', 'Tags']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    # Read hostvar .yml files in filelist
    for file in filelist:
        if file.endswith(".yml"):
            with open(path + file) as open_file:
                host = yaml.load(open_file)

                # Regex filters
                tag_finder = re.compile(regex_tags, re.IGNORECASE)
                ip_finder = re.compile(r'(\d+\.\d+\.\d+\.\d+)\/\d+')

                # Fine and store necessary information from hostvar.yml files
                if 'name' in host and 'mgmt_ip' in host:
                    name = host['name']
                    tag_match = tag_finder.search(name)
                    if tag_match:
                        tag = profile_prefix + '_' + tag_finder.sub(r'\1', host['name'])
                        command = 'ssh USER_NAME@' + ip_finder.sub(r'\1', host['mgmt_ip'])

                        # write rows in the csv file
                        writer.writerow({fields[0]: name, fields[1]: command, fields[2]: tag})
                        profiles += 1
                        # print(name + ',' + command + ',' + tag)  # This line is for debug use
                    else:
                        print(f"Skipping {name}: Matching tag not found'")
                else:
                    print(f"Skipping {file_name}: missing 'name' or 'mgmt_ip'")

print(f"\nProfiles created: {profiles}")