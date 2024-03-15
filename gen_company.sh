#!/usr/bin/env bash

USER_NAME=$1
if [ -z "${USER_NAME}" ]; then
    echo "User name for Arista SSH:"
    read USER_NAME
fi
USER_NAME=${USER_NAME} python3 gen_it2_profile.py company_iterm.csv ~/Library/Application\ Support/iTerm2/DynamicProfiles/Profiles_company.json
