import sys

import graphviz
from svgelements import Group, SVG

from common import get_input


class Comp:
    def __init__(self, lbl):
        self.lbl = lbl
        self.conn = set()

    def get_connected(self):
        to_expand = list(self.conn)
        conned = set()
        while to_expand:
            comp = to_expand.pop(0)
            if comp not in conned:
                conned.add(comp)
                for node in comp.conn:
                    if node not in conned:
                        to_expand.append(node)
        return conned


comps = {}
connections = set()
for entry in get_input(25):
    l, r = entry.split(": ")
    r = r.split()
    for comp in (l, *r):
        if comp not in comps:
            comps[comp] = Comp(comp)

    lcomp = comps[l]
    for comp in r:
        rcomp = comps[comp]
        if lcomp not in rcomp.conn or rcomp not in lcomp.conn:
            connections.add((l, comp))
            rcomp.conn.add(lcomp)
            lcomp.conn.add(rcomp)


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
        lc, rc = comps[l], comps[r]
        lc.conn.remove(rc)
        rc.conn.remove(lc)

    nodes = list(comps.values())
    connected1 = len(nodes[0].get_connected())
    print("Answer:", connected1 * (len(nodes) - connected1))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        part1()
    elif len(sys.argv) == 3:
        part2(sys.argv[1], sys.argv[2])
