#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from gexf import Gexf


def generate_graph():
    gexf = Gexf("sna - meetup.com", "A meetup.com social network analysis")
    graph = gexf.addGraph("directed", "static", "Meetup groups graph")

    groups = get_data('../data/groups.json')
    members = get_data('../data/members.json')

    # print groups[0]
    # print members[0]

    print "Total number of groups: %s" % len(groups)
    for index, group in enumerate(groups):
        graph.addNode(
            group.get('id'),
            group.get('urlname')
        )

    print "Total number of members: %s" % len(members)
    for index, member in enumerate(members):
        print index + 1
        name = member.get('name')
        if name:
            name = name.encode('ascii', 'ignore')
        else:
            name = ""
        graph.addNode(
            member.get('member_id'),
            name
        )
        graph.addEdge(
            index,
            member.get('group_id'),
            member.get('member_id')
        )

    return gexf


def get_data(path):
    with open(path) as data_file:
        return json.load(data_file)


def generate_xml(gexf):
    output_file = open("../graphs/groups.gexf", "w")
    gexf.write(output_file)


# main method
if __name__ == "__main__":
    graph = generate_graph()
    generate_xml(graph)