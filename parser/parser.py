#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Parser
'''

from .lex import Lex
from .procedure import start
from graphviz import *


class Parser:
    '''
    input sql and decide what action should be executed
    '''
    def __init__(self, sql):
        lex = Lex(sql)
        its = lex.get_iterator()
        self.status, self.header, self.leaves = start(lex, its)
        self.tree = []
        self.timer = 0
        self.create_tree()

    def show_nodes(self):
        print(len(self.header))
        for i in range(len(self.leaves)):
            print(self.header[i])
            for leave in self.leaves[i]:
                print( leave)

    def create_tree(self):
        dot = Digraph(comment='Tree')
        # dot.node('A', 'King Arthur')
        index = len(self.header) - 1

        parent = self.header[index]
        parent_id = str(self.get_timer())
        parent.set_id(parent_id)
        self.tree.append(parent)

        dot.node(parent.get_id(), parent.get_lable())
        self.do_insert_into_tree(dot, parent_id, index)

        while index > 0:
            index -= 1
            for token in self.tree[::-1]:
                if token.is_state() and self.header[index] == token:
                    token.mark_it()
                    parent_id = token.get_id()
                    self.do_insert_into_tree(dot, parent_id, index)
                    break
        dot.render('./round-table.gv', view=True)

    def do_insert_into_tree(self, dot, parent_id, index):
        for leaf in self.leaves[index]:
            leaf.set_id(str(self.get_timer()))
            leaf.set_parent(parent_id)
            dot.node(leaf.get_id(), leaf.get_lable())
            dot.edge(parent_id, leaf.get_id())
            self.tree.append(leaf)

    def get_timer(self):
        self.timer += 1;
        return self.timer




        return self.create_tree(index - 1)


