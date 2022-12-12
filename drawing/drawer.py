import os

import networkx as nx
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import sys

import pygraphviz


class Drawer:
    def __init__(self):
        self.G =None
    def pygraphviz_layout_with_rank(self, G, prog="dot", root=None, sameRank=[], args=""):  # Layout for AST

        if root is not None:  # add root to args for pygraphviz
            args += "-Groot=%s" % root  # add root to args for pygraphviz
        A = nx.nx_agraph.to_agraph(G)  # create a new graph with pygraphviz
        for sameNodeHeight in sameRank:  # add same rank nodes
            if type(sameNodeHeight) == str:  # if sameNodeHeight is a string
                print("node \"%s\" has no peers in its rank group" %
                      sameNodeHeight)  # print error message
            A.add_subgraph(sameNodeHeight, rank="same")  # add same rank nodes
        A.layout(prog=prog, args=args)  # layout with pygraphviz
        node_pos = {}  # empty dictionary to store positions
        for n in G:  # write pos into node_pos
            node = pygraphviz.Node(A, n)  # get node from pygraphviz
            try:  # try to get position
                xx, yy = node.attr["pos"].split(',')  # split position
                node_pos[n] = (float(xx), float(yy))  # write position
            except:  # if no position found for node n
                print("no position for node", n)  # print error message
                node_pos[n] = (0.0, 0.0)  # write position
        return node_pos  # return node_pos


    def draw_AST(self, same_rank_nodes):  # Draw AST
        graph = self.G  # nx.DiGraph()
        pos = self.pygraphviz_layout_with_rank(graph, prog='dot', sameRank=same_rank_nodes)

        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))  # labels for nodes
        f = plt.figure(1, figsize=(13, 8.65))  # figure size
        for shape in ['s', 'o']:  # draw nodes
            nx.draw_networkx_nodes(graph, pos, node_color='b', node_size=1300, node_shape=shape, label=labels, nodelist=[
                sNode[0] for sNode in filter(lambda x: x[1]["shape"] == shape, graph.nodes(data=True))])  # draw nodes
        nx.draw_networkx_edges(graph, pos, arrows=False)  # draw edges
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=7,font_color="white")  # draw labels
        f.canvas.manager.window.wm_geometry("+%d+%d" % (600, 0))  # set window position
        plt.show()  #  show graph

    def Draw(self,nodes_table,edges_table ,same_rank_nodes):  # Method to draw AST

        nodes_list = nodes_table  # get nodes table from parser
        edges_list = edges_table  # get edges table from parser
        self.G = nx.DiGraph()  # create graph
        print(nodes_list.items())
        for node_number, node in nodes_list.items():  # add nodes to graph
            self.G.add_node(node_number, value=node[0] + '\n' + node[1], shape=node[2])  # add nodes to graph
        self.G.add_edges_from(edges_list)  # add edges to graph

        self.draw_AST(same_rank_nodes)  #  draw graph