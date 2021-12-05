class Node:
    syn = 0
    inh = 0
    value = 0    

    def __init__(self, token: str, children: list):
        self.token = token
        self.children = children

    def add_child(self, child: 'Node'):
        self.children.append(child)
