#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib
import json
import sys
import requests

# Get api key from environment variable
# Get your key at https://secure.meetup.com/meetup_api/key/
API_KEY = os.environ['API_KEY']

# Define city to limit groups query
city = {
    'name': urllib.quote("Zürich"),
    'lon': '8.53999996185',
    'lat': '47.3800010681',
    'radius': '25.0'
}


# get meetup groups
def get_groups():
    print "running get_groups"

    # api request vars
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

    # get collection data from api request
    groups = get_collection_data(url, payload)

    # save data
    write_data(groups, '../data/groups.json')


# get meetup members of groups
def get_members():
    print "running get_members"

    groups = None
    group_members = []

    # load groups data
    with open('../data/groups.json') as data_file:
        groups = json.load(data_file)

    # test group
    # groups = [{'id': '19008715'}, {'id': '19056459'}]

    for index, group in enumerate(groups):
        index += 1
        print "%s in %s, group_id: %s" % (index, len(groups), group['id'])
        # print "members count: %s" % group['members']

        payload = {
            'group_id': group.get('id'),
            'sign': 'True',
            'format': 'json',
            'page': '200',
            'only': 'id,name,country,city,joined',
            'key': API_KEY
        }

        url = "https://api.meetup.com/2/members"

        print 'fetching member data'
        members = get_collection_data(url, payload)

        print 'building group member collection'
        for member in members:
            group_members.append({
                'group_id': group.get('id'),
                'member_id': member.get('id'),
                'name': member.get('name'),
            })
        print "group_id: %s, members: %s" % (group.get('id'), len(members))
        print

    print "Total number of members: %s" % len(group_members)
    write_data(group_members, '../data/members.json')


def get_collection_data(url, payload):
    # get the data
    collection = []

    # run api request
    data = get_data(url, payload)

    # get the next url to crawl (paged api)
    next_page = data['meta']['next']

    # extend collection list with new data list
    collection.extend(data['results'])

    # run as long as there's a next page available
    while next_page != "":

        # catch connection timeout
        try:
            data = get_data(next_page, payload)
        except requests.exceptions.ConnectionError as e:
            print "Raised %s, trying again" % e
            data = get_data(next_page, payload)

        # define next page
        next_page = data['meta']['next']

        collection.extend(data['results'])

    return collection


def get_data(url, payload):
    # get json data from api
    r = requests.get(url, params=payload)
    return r.json()


def write_data(data, path):
    # save data as json to file
    with open(path, 'w+') as outfile:
        json.dump(data, outfile)


# main method
if __name__ == "__main__":

    # look for command-line arguments
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
