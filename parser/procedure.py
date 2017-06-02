#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
start -> sql_select
        | sql_projection

sql_select -> select [ condiction ] ( table )

sql_projection -> projection [ columns ] ( table )

condiction -> id op value A

op -> =
    | <
    | >

A -> null
    | & condiction

columns -> id B

B -> null
    | , columns

table -> id C
    | sql_select C
    | sql_projection C
    | avg [ columns ] table
C -> null
    | join table

'''

from .token import Token


tmp = []
leaves = []
header = []

def deal_error(token):
    print('Error', token)
    return False

def fill_tmp(i, token, source):
    if source[i] == 'value' or source[i] == 'id':
        tmp[-1].append(token)
    elif source[i] != None:
        tmp[-1].append(Token(source[i], True))
    else:
        if not token.no_use():
            tmp[-1].append(token)

def do_rollback(lex, times):
    for i in range(times):
        lex.rollback()

def do_action(lex, its, source, action, is_func, special = ()):
    times = 0
    token = None
    for i in range(len(action)):
        if is_func[i]:
            if i in special:
                token = lex.lookahead(its)
                times += 1
            r = eval(action[i])
        else:
            token = lex.lookahead(its)
            times += 1
            r = token.equal(action[i])
        fill_tmp(i, token, source)
        if not r:
            do_rollback(lex, times)
            return False
    return True

def start(lex, its):
    '''
    the start of parser
    start -> sql_select | sql_projection
    '''
    print("# start")
    if sql_select(lex, its):
        print("start -> sql_select")
        header.append(Token('start', True))
        leaves.append([Token('sql_select', True)])
        return True, header, leaves
    if sql_projection(lex, its):
        print("start -> sql_projection")
        header.append(Token('start', True))
        leaves.append([Token('sql_projection', True)])

        return True, header, leaves
    return False

def sql_select(lex, its):
    '''
    sql_select -> select [ condiction ] ( table )

    '''
    print("# select")

    tmp.append([])
    source = (None, None, 'condiction', None, None, 'table', None)
    action = ('select', '[', 'condiction(lex, its)', ']', '(', 'table(lex, its)', ')')
    is_func = (False, False, True, False, False, True, False)

    if do_action(lex, its, source, action, is_func):
        print('sql_select -> select [ condiction ] ( table )')
        header.append(Token('sql_select', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    tmp.pop()
    return False

def sql_projection(lex, its):
    '''
    sql_projection -> projection [ columns ] ( table )
    '''
    print("# projection")

    tmp.append([])
    source = (None, None, 'columns', None, None, 'table', None)
    action = ('projection', '[', 'columns(lex, its)', ']', '(', 'table(lex, its)', ')')
    is_func = (False, False, True, False, False, True, False)

    if do_action(lex, its, source, action, is_func):
        print("sql_projection -> projection [ columns ] ( table) ")
        header.append(Token('sql_projection', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    tmp.pop()
    return False

def condiction(lex, its):
    '''
    condiction -> id op value A
    '''
    print("# condiction")

    tmp.append([])
    source = ('id', 'op', 'value', 'A')
    action = ('token.is_id()', 'op(lex, its)', 'token.is_value()', 'A(lex, its)')
    is_func = (True, True, True, True)
    special = (0, 2)
    if do_action(lex, its, source, action, is_func, special):
        print("condiction -> id op value A")
        header.append(Token('condiction', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    tmp.pop()
    return False
def op(lex, its):
    '''
    op -> =
    | <
    | >
    '''
    print("# op")

    token = lex.lookahead(its)
    if token.equal('='):
        print('op -> =')
        header.append(Token('op', True))
        leaves.append([token])
        return True
    elif token.equal('<'):
        print('op -> <')
        header.append(Token('op', True))
        leaves.append([token])
        return True
    elif token.equal('>'):
        print('op -> >')
        header.append(Token('op', True))
        leaves.append([token])
        return True
    return False

def A(lex, its):
    '''
    A -> null
    | & condiction
    '''
    print("# A")

    tmp.append([])

    source = (None, 'condiction')
    action = ('&', 'condiction(lex, its)')
    is_func = (False, True)
    if do_action(lex, its, source, action, is_func):
        print('A-> & condiction')
        header.append(Token('A', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print('A -> null')
    header.append(Token('A', True))
    leaves.append([Token(None, True)])
    tmp.pop()
    return True

def columns(lex, its):
    '''
    columns -> id B
    '''
    print("# columns")

    tmp.append([])

    source = ('id', 'B')
    action = ('token.is_id()', 'B(lex, its)')
    is_func = (True, True)
    special = (0, )
    if do_action(lex, its, source, action, is_func, special):
        print('columns -> id B')
        header.append(Token('columns', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    tmp.pop()
    return False

def B(lex, its):
    '''
    B -> null
    | , columns
    '''
    print("# B")

    tmp.append([])
    source = (None, 'columns')
    action = (',', 'columns(lex, its)')
    is_func = (False, True)
    if do_action(lex, its, source, action, is_func):
        print('B -> , columns')
        header.append(Token('B', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print('B -> null')
    header.append(Token('B', True))
    leaves.append([Token(None, True)])
    tmp.pop()
    return True

def table(lex, its):
    '''
    table -> id C
    | sql_select C
    | sql_projection C
    | avg [ columns ] table
    '''
    print("# table id c")

    tmp.append([])
    source = ('id', 'C')
    action = ('token.is_id()', 'C(lex, its)')
    is_func = (True, True)
    special = (0,)
    if do_action(lex, its, source, action, is_func, special):
        print('table -> id C')
        header.append(Token('table', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print("# table select c")

    tmp[-1] = []
    source = ('sql_select', 'C')
    action = ('sql_select(lex, its)', 'C(lex, its)')
    if do_action(lex, its, source, action, is_func):
        print('table -> sql_select C')
        header.append(Token('table', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print("# table projection c")

    tmp[-1] = []
    source = ('sql_projection', 'C')
    action = ('sql_projection(lex, its)', 'C(lex, its)')
    if do_action(lex, its, source, action, is_func):
        print('table -> sql_projection C')
        header.append(Token('table', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print("# table avg")

    tmp[-1] = []
    source = (None, None, 'columns', None, None, 'table', None)
    action = ('avg', '[', 'columns(lex, its)', ']', '(', 'table(lex, its)', ')')
    is_func = (False, False, True, False, False, True, False)
    if do_action(lex, its, source, action, is_func):
        print('table ->  avg [ columns ] table')
        header.append(Token('table', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    tmp.pop()
    return False


def C(lex, its):
    '''
    C -> null
    | join table
    '''
    print("# C")

    tmp.append([])
    source = (None, 'table')
    action = ('join', 'table(lex, its)')
    is_func = (False, True)
    if do_action(lex, its, source, action, is_func):
        print('C -> join table')
        header.append(Token('C', True))
        leaves.append(tmp[-1])
        tmp.pop()
        return True
    print('C -> null')
    header.append(Token('C', True))
    leaves.append([Token(None, True)])
    tmp.pop()
    return True
