#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Lex
'''
from .token import Token
from .const import *
from string import digits
class Lex:
    '''lex'''
    def __init__(self, sql):
        self.tokens = sql.split(' ')
        self.index = 0

    def get_iterator(self):
        ''''
        get iterator
        '''
        while True:
            if self.index >= len(self.tokens):
                yield Token(None)
            else:
                input = self.tokens[self.index]
                print("->    %s" % input)
                yield Token(input)
            self.index += 1
    def lookahead(self, its):
        return next(its)
    def rollback(self):
        if self.index > -1:
            self.index -= 1
