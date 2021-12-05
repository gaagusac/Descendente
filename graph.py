import node
import graphviz

dot = graphviz.Graph(format="png")

def create_gv(root: node.Node):
    if not root: return
    # print(root.token)
    label = ''
    if root.token == '+' \
        or root.token == '-' \
        or root.token == '*' \
        or root.token == '/' \
        or root.token == '(' \
        or root.token == ')' \
        or root.token == 'ε' \
        or root.token == 'n':
        label = f'{root.token}'
    elif root.token == "T'" or root.token == "E'":
        label = f'{root.token}.inh = {root.inh} \\n {root.token}.syn = {root.syn}'
    else:
        label = f'{root.token}.val = {root.value}'
    dot.node(str(hash(root)), label, shape='plaintext')
    if not root.children: return
    for ch in root.children:
        dot.edge(str(hash(root)), str(hash(ch)))
    for child in root.children:
        create_gv(child)

def view_gv(title="title goes here"):
    dot.attr(label=title)
    dot.attr(labelloc="top")
    dot.attr(labeljust="left")
    dot.view()
    dot.clear()