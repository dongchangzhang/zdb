from graphviz import *
dot = Digraph(comment='The Round Table')
dot.node('B', 'B')
dot.node('L', 'L')
dot.node('L', 'L')

dot.node('A', 'A')
dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')
print(dot.source)
dot.render('./round-table.gv', view=True)