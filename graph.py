#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from gexf import Gexf


def generate_graph():
    gexf = Gexf("sna - meetup.com", "A meetup.com social network analysis")
    graph = gexf.addGraph("undirected", "static", "Meetup groups graph")

    # attributes
    organizer_attr = graph.addNodeAttribute('organizer', 'None', 'string')
    type_attr = graph.addNodeAttribute('type', 'None', 'string')
    category_attr = graph.addNodeAttribute('category', 'None', 'integer')

    groups = get_data('data/groups.json')
    members = get_data('data/members.json')

    # print groups[0]
    # print members[0]

    print "Total number of groups: %s" % len(groups)

    for index, group in enumerate(groups):
        node = graph.addNode(
            "G-%s" % group.get('id'),
            group.get('urlname')
        )
        if group.get('organizer'):
            node.addAttribute(organizer_attr, str(group.get('organizer').get('member_id')))
        if group.get('category'):
            node.addAttribute(category_attr, str(group.get('category').get('id')))
        node.addAttribute(type_attr, 'Group')

    print "Total number of members: %s" % len(members)

    for index, member in enumerate(members):
        # print index + 1

        node = graph.addNode(
            "M-%s" % member.get('member_id'),
            get_member_name(member.get('name'))
        )
        node.addAttribute(type_attr, 'Member')

        graph.addEdge(
            index,
            "G-%s" % member.get('group_id'),
            "M-%s" % member.get('member_id'),
        )

    return gexf


def get_member_name(name):
    if name:
        name = name.encode('ascii', 'ignore')
    else:
        name = ""
    return name


def get_data(path):
    with open(path) as data_file:
        return json.load(data_file)


def generate_xml(gexf):
    output_file = open("graphs/groups.gexf", "w")
    gexf.write(output_file)


# main method
if __name__ == "__main__":
    graph = generate_graph()
    generate_xml(graph)
