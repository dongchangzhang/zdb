#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Lex
'''
class Lex:
    '''lex'''
    def __init__(self, sql):
        self.tokens = sql.split(' ')
        self.index = 0

    def lookahead(self):
        ''''
        get next token
        '''
        while len(self.tokens) > self.index:
            yield self.tokens[self.index]
            self.index += 1
        yield None
