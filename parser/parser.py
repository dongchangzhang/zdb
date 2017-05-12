#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Parser
'''

from .lex import Lex

class Parser:
    '''
    input sql and decide what action should be executed
    '''
    def __init__(self, sql):
        lex = Lex(sql)
        its = lex.lookahead()
        print(next(its))



