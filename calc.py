import node
import ply.yacc as yacc
import ply.lex as lex
import graph
tokens = ('number', 'plus', 'minus', 'times', 'divide', 'lparen', 'rparen')
t_plus = r'\+'
t_minus = r'-'
t_times = r'\*'
t_divide = r'/'
t_lparen = r'\('
t_rparen = r'\)'


def t_number(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
# Grammar
# 1) E -> T E'
# 2) E' -> + T E'
# 3)    -> - T E'
# 4)    | ε
# 5) T -> F T'
# 6) T' -> * F T'
# 7)    | / F T'
# 8)    | ε
# 9) F -> ( E )
# 10)   | DIGIT


def p_p1(t):
    'E : T Ep'
    enode = node.Node('E', [])
    enode.add_child(t[1])
    enode.add_child(t[2])
    enode.value = t[2].syn # Synth
    t[0] = enode


def p_p2(t):
    'Ep : plus T Ep'
    epnode = node.Node("E'", [])
    epnode.inh = t[-1].value # Inherit
    epnode.syn = epnode.inh + t[3].syn # Synth
    epnode.add_child(node.Node('+', []))
    epnode.add_child(t[2])
    epnode.add_child(t[3])
    t[0] = epnode


def p_p3(t):
    'Ep : minus T Ep'
    epnode = node.Node("E'", [])
    epnode.inh = t[-1].value # Inherit
    epnode.syn = epnode.inh - t[3].syn # Synth
    epnode.add_child(node.Node('-', []))
    epnode.add_child(t[2])
    epnode.add_child(t[3])
    t[0] = epnode


def p_p4(t):
    'Ep : '  # Empty
    epnode = node.Node("E'", [])
    epnode.inh = epnode.syn = t[-1].value # Inherit
    epsilonnode = node.Node('ε', [])
    epnode.add_child(epsilonnode)
    t[0] = epnode


def p_p5(t):
    'T : F Tp'
    tnode = node.Node('T', [])
    tnode.add_child(t[1])
    tnode.add_child(t[2])
    tnode.value = t[2].syn # Synth
    t[0] = tnode


def p_p6(t):
    'Tp : times F Tp'
    tpnode = node.Node("T'", [])
    tpnode.inh = t[-1].value # Inherit
    tpnode.syn = tpnode.inh * t[3].syn # Syth
    tpnode.add_child(node.Node('*', []))
    tpnode.add_child(t[2])
    tpnode.add_child(t[3])
    t[0] = tpnode


def p_p7(t):
    'Tp : divide F Tp'
    tpnode = node.Node("T'", [])
    tpnode.inh = t[-1].value # Inherit
    tpnode.syn = tpnode.inh / t[3].syn # Synth
    tpnode.add_child(node.Node('/', []))
    tpnode.add_child(t[2])
    tpnode.add_child(t[3])
    t[0] = tpnode


def p_p8(t):
    'Tp : '
    tpnode = node.Node("T'", [])
    tpnode.inh = tpnode.syn = t[-1].value # inherit
    epsilonnode = node.Node('ε', [])
    tpnode.add_child(epsilonnode)
    t[0] = tpnode


def p_p9(t):
    'F : lparen E rparen'
    fnode = node.Node('F', [])
    fnode.value = t[2].value # Synth
    fnode.add_child(node.Node('(', []))
    fnode.add_child(t[2])
    fnode.add_child(node.Node(')', []))
    t[0] = fnode


def p_p10(t):
    'F : number'
    fnode = node.Node('F', [])
    numbernode = node.Node('number', [])
    numbernode.value = int(t[1])
    fnode.add_child(numbernode)
    fnode.value = numbernode.value # Synth
    t[0] = fnode


parser = yacc.yacc()
end_marker = "n"
analisis_type = "   (Descendente)"
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    root = parser.parse(s)
    root.add_child(node.Node('n', [])) # End of input marker
    graph.create_gv(root)
    graph.view_gv(s+end_marker+analisis_type)