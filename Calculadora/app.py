from flask import Flask, request, jsonify, render_template
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree

# Definición de los tokens
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
)

# Expresiones regulares para los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+'

# Ignorar los espacios en blanco y las tabulaciones
t_ignore = ' \t'

# Función para manejar errores de token
def t_error(t):
    print("Error: Caracter inesperado '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = Node('+', children=[p[1], p[3]])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = Node('-', children=[p[1], p[3]])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = Node('*', children=[p[1], p[3]])

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = Node('/', children=[p[1], p[3]])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = Node(p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = Node('()', children=[Node('(', children=[]), p[2], Node(')', children=[])])

def p_error(p):
    print("Error de sintaxis")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Creación de la aplicación Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', resultado_lexico='', arbol='')

@app.route('/analizar', methods=['POST'])
def analizar():
    expresion = request.json['expresion']
    lexer.input(expresion)
    resultado_lexico = [(token.type, token.value) for token in lexer]
    arbol = parser.parse(expresion)

    return jsonify({
        'resultado_lexico': resultado_lexico,
        'arbol': RenderTree(arbol).by_attr() if arbol else ''
    })

if __name__ == '__main__':
    app.run(debug=True)
