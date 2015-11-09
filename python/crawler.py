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

    groups = get_collection_data(url, payload)

    write_data(groups, '../data/groups.json')


def get_members():
    print "running get_members"

    groups = None
    group_members = []

    with open('../data/groups.json') as data_file:
        groups = json.load(data_file)

    # groups = [{'id': '7059'}]

    for group in groups:
        print "group_id: %s" % group['id']
        # print "members count: %s" % group['members']

        payload = {
            'group_id': group['id'],
            'sign': 'True',
            'format': 'json',
            'page': '200',
            'key': API_KEY
        }

        url = "https://api.meetup.com/2/members"

        print 'fetching member data'
        members = get_collection_data(url, payload)

        print 'building group member colletionc'
        for member in members:
            group_members.extend({
                'group_id': group['id'],
                'member_id': member['id'],
                'name': member['name'],
            })

    write_data(group_members, '../data/members.json')


def get_collection_data(url, payload):
    # get the data
    collection = []

    data = get_data(url, payload)
    next_page = data['meta']['next']
    collection.extend(data['results'])

    while next_page != "":
        data = get_data(next_page, payload)
        next_page = data['meta']['next']
        collection.extend(data['results'])

    return collection


def get_data(url, payload):
    r = requests.get(url, params=payload)
    return r.json()


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
