import ply.lex as lex
import ply.yacc as yacc

# Variables globales para almacenar resultados
resultado_lexema = []
resultado_sintactico = []
errores = []
token_count = {}

# Palabras reservadas
reservada = {
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'do': 'DO',
    'float': 'FLOAT',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'class': 'CLASS',
    'return': 'RETURN',
    'new': 'NEW',
    'int': 'INT',
    'programa': 'PROGRAMA',
    'read': 'READ',
    'printf': 'PRINTF',
    'end': 'END',
    'System': 'SYSTEM', 
    'out': 'OUT', 
    'println': 'PRINTLN'
}

tokens = list(reservada.values()) + [
    'identificador', 'NUMERO', 'PUNTO', 'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER',
    'IGUAL', 'MAS', 'MAYORIGUAL', 'MENORIGUAL', 'MASMAS', 'COMA', 'PUNTOYCOMA', 'CADENA'
]

# Expresiones regulares para tokens simples
t_PUNTO = r'\.'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_IGUAL = r'='
t_MAS = r'\+'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MASMAS = r'\+\+'
t_COMA = r','
t_PUNTOYCOMA = r';'
t_CADENA = r'\".*?\"'

# Definición de tokens para números y variables
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_identificador(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservada.get(t.value, 'identificador')  # Verifica si es una palabra reservada
    return t

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores de tokens no válidos
def t_error(t):
    global resultado_lexema
    resultado_lexema.append({"token": "ERROR", "lexema": t.value, "linea": t.lineno})
    t.lexer.skip(1)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Función para analizar el texto ingresado (léxico)
def prueba_lexico(data):
    global resultado_lexema, token_count
    resultado_lexema.clear()  # Limpiar la lista antes de cada prueba
    token_count.clear()  # Limpiar el contador de tokens
    analizador = lex.lex()
    analizador.input(data)

    while True:
        tok = analizador.token()
        if not tok:
            break
        resultado_lexema.append({"token": tok.type, "lexema": tok.value, "linea": tok.lineno})
        
        # Contar tokens
        if tok.type in token_count:
            token_count[tok.type] += 1
        else:
            token_count[tok.type] = 1

# Reglas gramaticales para el pseudocódigo
def p_programa(p):
    '''programa : PROGRAMA def PARIZQ PARDER LLAVEIZQ code LLAVEDER'''
    p[0] = ('programa', p[2], p[5])

def p_def(p):
    '''def : identificador'''
    p[0] = p[1]  # Almacena el identificador

def p_code(p):
    '''code : expr'''
    p[0] = p[1]

def p_expr(p):
    '''expr : INT ids PUNTOYCOMA
            | READ identificador PUNTOYCOMA 
            | op
            | PRINTF PARIZQ CADENA PARDER PUNTOYCOMA
            | END PUNTOYCOMA
            | expr expr'''
    
    # Manejo de la expresión
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('composición', p[1], p[2])

def p_op(p):
    '''op : identificador IGUAL identificador MAS identificador PUNTOYCOMA'''
    p[0] = ('asignación', p[1], p[3], p[5])  # Almacena la operación

def p_ids(p):
    '''ids : identificador 
           | ids COMA identificador'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Error de sintaxis
def p_error(p):
    if p:
        errores.append(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        errores.append("Error de sintaxis: fin de entrada inesperado")

# Función para el análisis sintáctico
def prueba_sintactico(data):
    global resultado_sintactico, errores
    resultado_sintactico.clear()  # Limpiar el resultado antes de cada prueba
    errores.clear()  # Limpiar la lista de errores
    parser = yacc.yacc()
    parser.parse(data, lexer=lex.lex())
    if errores:
        resultado_sintactico.extend(errores)
    else:
        resultado_sintactico.append("Análisis sintáctico correcto")
