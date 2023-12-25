from collections import defaultdict
import sys

import graphviz
from svgelements import Group, SVG

from common import get_input


comps = defaultdict(set)
connections = set()
for entry in get_input(25):
    l, r = entry.split(": ")
    lcomp = comps[l]
    for r in r.split():
        rcomp = comps[r]
        if lcomp not in rcomp or rcomp not in lcomp:
            connections.add((l, r))
            rcomp.add(l)
            lcomp.add(r)


def part1():
    dot = graphviz.Digraph('dot', format='svg')
    for comp in comps.keys():
        dot.node(comp)
    for l, r in connections:
        dot.edge(l, r)
    dot.render()


def part2(l='dvp', r='ngs'):
    with open('dot.gv.svg') as f:
        root = SVG.parse(f)

    node_xs = {
        node[0].title: node[1].cx for node in root[0]
        if isinstance(node, Group) and node.values["class"] == "node"
    }
    midway = (node_xs[r] + node_xs[l]) / 2
    to_remove = [(l, r) for l, r in connections if (node_xs[l] < midway) != (node_xs[r] < midway)]
    assert len(to_remove) == 3

    for l, r in to_remove:
        comps[l].remove(r)
        comps[r].remove(l)

    nodes = list(comps.keys())
    to_expand = list(comps[nodes[0]])
    conned = set()
    while to_expand:
        comp = to_expand.pop(0)
        if comp not in conned:
            conned.add(comp)
            for node in comps[comp]:
                if node not in conned:
                    to_expand.append(node)

    connected1 = len(conned)
    print("Answer:", connected1 * (len(nodes) - connected1))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        part1()
    elif len(sys.argv) == 3:
        part2(sys.argv[1], sys.argv[2])
