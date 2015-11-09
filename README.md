# sna

social network analysis course project based on meetup.com data.

## Crawler

Fetches data from groups in Zurich and their members and stores in in json files.

### Install

    pip install requests

### Run

Get your API key at https://secure.meetup.com/meetup_api/key/

    cd python

    env API_KEY='<YOUR_API_KEY>' python crawler.py get_groups get_members
