#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import urllib
import json
import sys

# Get your key at https://secure.meetup.com/meetup_api/key/
API_KEY = os.environ['API_KEY']
CITY = urllib.quote("Zürich")


def get_groups():
    print "running get_groups"
    # groups in city of zurich
    API_URL = "https://api.meetup.com/2/groups?country=ch&city=%s&sign=True&format=json&lon=8.53999996185&photo-host=public&radius=25.0&fields=&lat=47.3800010681&order=id&desc=false&key=%s" % (CITY, API_KEY)

    # get the data
    r = requests.get(API_URL)
    data = r.json()

    write_data(data, '../data/groups.json')


def get_members():
    print "running get_members"
    # API_URL = "https://api.meetup.com/2/members?&sign=true&photo-host=public&group_id=%s" % (group_id)


def write_data(data, file):
    with open(file, 'w+') as outfile:
        json.dump(data, outfile)

# main method
if __name__ == "__main__":
    for arg in sys.argv:

        if 'get_groups' in arg:
            get_groups()

        if 'get_members' in arg:
            get_members()

        if len(sys.argv) is 1:
            print "Usage:"
            print "env API_KEY='<YOUR_APIKEY>' python crawler.py get_groups get_members"
            print "Get your key at https://secure.meetup.com/meetup_api/key/"
