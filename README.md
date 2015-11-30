# sna

Social Network Analysis course project based on **meetup.com** data.

## Crawler

Fetches data from *groups* in Zurich and their *members* and stores in in JSON files.

## Graph-Export

Exports a Gephi-compatible `.gexf` file with groups and member nodes/edges.

## Development setup

### Dependencies

- requests
- lxml
- pygexf

### Setup

    # Create a virtualenv
    mkvirtualenv sna

    # Install dependencies
    pip install -r REQUIREMENTS

### Usage

    # Activate virtualenv
    workon sna

    # Get your API key at https://secure.meetup.com/meetup_api/key/

    # Crawl groups and members data from meetup
    env API_KEY='<YOUR_API_KEY>' python crawler.py get_groups get_members

    # Generate Gephi graph
    graph.py
