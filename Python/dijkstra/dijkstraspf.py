#! /usr/bin/python3
"""
SPDX-FileCopyrightText: 2019 Alan De Smet <chaos@highprogrammer.com>
SPDX-License-Identifier: GPL-3.0-or-later

Copyright (C) 2019 Alan De Smet

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
"""

from math import inf as _infinity

class GraphPaths:
    """
    Represents a set of paths from some origin to a single destination

    Returned by dijkstra_spf.
    """
    def __init__(self, dst_name):
        """ Initialize self with a destination of dst_name """
        self.dst_name = dst_name
        self.previous = None
        self.distance = _infinity

    def add_possible_route(self, previous, distance):
        """ Add a route if it's not longer than existing routes

        If the new route is shorter than existing routes, the
        previous, longer routes will be discarded.
        """
        if distance > self.distance:
            return
        elif distance == self.distance:
            self.previous.append(previous)
        else: # distance > self.distance
            self.distance = distance
            self.previous = [ previous ]

    def allpaths(self):
        """ Return list of all shortest paths

        Each path is a list of names.
        """
        results = []
        if self.previous is None:
            return [[self.dst_name]]
        for previous in self.previous:
            for path in previous.allpaths():
                results.append([self.dst_name] + path)
        return results

    def fullpath(self):
        """ Return an arbitrary shortest path as a list of names """
        p = [self.dst_name]
        x = self.previous[0]
        while x is not None:
            p.append(x.dst_name)
            x = x.previous[0]
        p.reverse()
        return p

    def __repr__(self):
        paths = [ ">".join(x) for x in self.allpaths() ]
        return "(Path to {}: {} {})".format(self.dst_name, self.distance, " ".join(paths))

def dijkstra_spf(graph, origin, bidirectional = True):
    """ Return shortest paths from origin to each node in graph

    Arguments:
    graph: iterable containing triplets of (start_node, end_node,
             distance).  distance is optional and defaults to 1
    origin: node all distances are computed from
    bidirectional: if True (the default), paths from end_node to
             start_node will automatically be included.

    Returns: a dict of {destination_name: GraphPaths}

    >>> from dijkstraspf import dijkstra_spf
    >>> from pprint import pformat
    >>> pformat(dijkstra_spf(
    ...     [('A', 'B', 3),
    ...      ('A', 'C', 1),
    ...      ('C', 'B', 1)],
    ...     'A'))
    "{'A': (Path to A: 0 A), 'B': (Path to B: 2 B>C>A), 'C': (Path to C: 1 C>A)}"
    """
    # Using pprint.pformat above to ensure result is sorted for reproducability

    # Build up a dict of (src,dst):length
    newgraph = {}
    remaining_nodes = set()
    def add_edge(src, dst, length):
        remaining_nodes.add(src)
        remaining_nodes.add(dst)
        if src not in newgraph:
            newgraph[src] = {}
        if dst in newgraph[src]:
            raise Exception("{}->{} is already in the graph. (Previous length {}, new length {})".format(src, dst, newgraph[src][dst], length))
        newgraph[src][dst] = length
    for edge in graph:
        src = edge[0]
        dst = edge[1]
        length = edge[2] if len(edge)>=3 else 1
        add_edge(edge[0], edge[1], edge[2])
        if bidirectional:
            add_edge(edge[1], edge[0], edge[2])
    graph = newgraph

    # Validate origin
    if origin not in remaining_nodes:
        raise Exception('Starting node "{}" is not in the graph'.format(origin))

    # Initialize results
    paths = {}
    for node in remaining_nodes:
        paths[node] = GraphPaths(node)
    paths[origin].distance = 0

    while len(remaining_nodes) > 0:
        nearest = min(remaining_nodes, key=lambda x: paths[x].distance)
        remaining_nodes.remove(nearest) 
        my_length = paths[nearest].distance

        neighbors = graph[nearest].keys()
        unfinished_neighbors = set(neighbors) & remaining_nodes
        for neighbor in unfinished_neighbors:
            newdist = my_length + graph[nearest][neighbor]
            paths[neighbor].add_possible_route(paths[nearest], newdist)

    return paths


################################################################################
#
# TESTING
#

import unittest
class _ExternalTest(unittest.TestCase):
    def test_external_graphs(self):
        for test in sorted(self._test_load_tests()):
            with self.subTest(msg=test.name):
                self._test_run_test(test)

    def _test_load_tests(self):
        """ Return list of _TestCases from test directory """
        import yaml
        import os.path
        testlist = []
        tests = _test_find_tests()
        for testfile in tests:
            with open(testfile) as f:
                data = yaml.safe_load(f)
                testname = testfile[:-len(".yaml")]
                testname = os.path.basename(testname)
                testlist.append(_TestCase(testname, data))
        return testlist

    def _test_run_test(self, test):
        """ Run a _TestCase """
        src = "A"
        paths = dijkstra_spf(test.graph, src)
        solutions = {}
        for destination in paths.values():
            for path in destination.allpaths():
                key = (src, destination.dst_name)
                if key not in solutions:
                    solutions[key] = []
                path.reverse()
                solutions[key].append(_TestSolution(destination.distance, path))
        for key in solutions.keys():
            solutions[key].sort()

        self.assertEqual(solutions, test.solutions)



def _test_find_tests():
    import os
    rootdir = os.path.dirname(__file__)
    testdir = os.path.join(rootdir, "test-data")
    if not os.path.isdir(testdir):
        raise Exception("Failed to find directory of test data at {}".format(testdir))
    testdata = os.path.join(testdir, "*.yaml")

    import glob
    results = []
    for graphfile in glob.iglob(testdata):
        if not os.path.isfile(graphfile):
            raise Exception("Test file {} is not a file.".format(graphfile))
        results.append(graphfile)
    return results

class _TestSolution:
    def __init__(self, length, path):
        self.length = length
        self.path = path
    def __str__(self):
        return "(solution length {}: {})".format(self.length, " ".join(self.path))
    def __repr__(self):
        return "({}: {})".format(self.length, " ".join(self.path))

    def __eq__(self, other):
        return self.length == other.length and self.path == other.path

    def __lt__(self, other):
        if self.length < other.length:
            return True
        if self.length > other.length:
            return False
        return self.path < other.path


class _TestCase:
    def __init__(self, name, data):
        self.name = name

        self.graph = []
        for edge in data['edges']:
            self.add_edge_record(edge)

        self.solutions = {}
        for solution in data['solutions']:
            self.add_solution_record(solution)
        for key in self.solutions:
            self.solutions[key].sort()

    def add_edge_record(self, record):
            fields = record.rstrip().lstrip().split(" ")
            if len(fields) >= 3:
                length = fields[2]
                fields[2] = float(length) if "." in length else int(length)
            self.graph.append(fields)

    def add_solution_record(self, record):
        length, rest = record.rstrip().split(" ",1)
        length = float(length) if "." in length else int(length)
        path = rest.split(" ")
        name = (path[0],path[-1])
        if name not in self.solutions:
            self.solutions[name] = []
        self.solutions[name].append(_TestSolution(length, path))
        
    def __repr__(self):
        return "({}: graph: {} / solutions: {})".format(self.name, self.graph, self.solutions)

    def __lt__(self, other):
        return self.name < other.name

def load_tests(loader, tests, ignore):
    import doctest
    tests.addTests(doctest.DocTestSuite())
    return tests

    
if __name__ == '__main__':
    unittest.main()


#graph = [
#        ("a", "b", 10),
#        ("b", "c", 5),
#        ("a", "c", 5),
#    ]
#print(dijkstra_spf(graph, "a"))
