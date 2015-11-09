#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import urllib
import json
import sys

# Get your key at https://secure.meetup.com/meetup_api/key/
API_KEY = os.environ['API_KEY']

city = {
    'name': urllib.quote("Zürich"),
    'lon': '8.53999996185',
    'lat': '47.3800010681',
    'radius': '25.0'
}


def get_groups():
    print "running get_groups"

    payload = {
        'country': 'ch',
        'lon': city.get('lon'),
        'lat': city.get('lat'),
        'radius': city.get('radius'),
        'sign': 'True',
        'format': 'json',
        'page': '200',
        'key': API_KEY
    }

    # groups in city of zurich
    url = "https://api.meetup.com/2/groups"

    data = get_groups_data(url, payload)
    groups = data['results']
    next_page = data['meta']['next']

    while next_page != "":
        data = get_groups_data(next_page, payload)
        groups.append(data['results'])
        next_page = data['meta']['next']

    write_data(groups, '../data/groups.json')


def get_groups_data(url, payload):
    # get the data
    r = requests.get(url, params=payload)
    return r.json()


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
            print

        if 'get_members' in arg:
            get_members()
            print

        if len(sys.argv) is 1:
            print "Usage:"
            print "env API_KEY='<YOUR_APIKEY>' python crawler.py get_groups get_members"
            print
            print "Get your key at https://secure.meetup.com/meetup_api/key/"
