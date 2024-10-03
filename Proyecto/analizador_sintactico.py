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
    'IGUAL', 'MAS', 'MAYORIGUAL', 'MENORIGUAL', 'MASMAS', 'COMA', 'PUNTOYCOMA', 'CADENA','END'
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
                

# # Reglas gramaticales para un bucle for
# def p_instruccion_for(p):
#     '''instruccion : FOR PARIZQ INT identificador IGUAL NUMERO PUNTOYCOMA identificador MENORIGUAL NUMERO PUNTOYCOMA identificador MASMAS PARDER bloque'''
#     p[0] = ('for', ('declaracion', p[3], p[4], p[6]), ('condicion', p[8], p[9]), ('incremento', p[11]), p[14])

# # Bloque de instrucciones dentro del bucle for
# def p_bloque(p):
#     '''bloque : LLAVEIZQ instruccion_llamada LLAVEDER'''
#     p[0] = ('bloque', p[2])

# # Llamada a System.out.println
# def p_instruccion_llamada(p):
#     '''instruccion_llamada : SYSTEM PUNTO OUT PUNTO PRINTLN PARIZQ CADENA MAS identificador PARDER PUNTOYCOMA'''
#     p[0] = ('println', p[7], p[9])


# Reglas gramaticales para el pseudocódigo
def p_programa(p):
    'programa : PROGRAMA identificador PARIZQ PARDER LLAVEIZQ declaraciones LLAVEDER'
    p[0] = ('programa', p[2], p[5])

def p_declaracion(p):
    'declaraciones : INT lista_identificadores PUNTOYCOMA instrucciones'
    p[0] = ('declaraciones', p[2], p[4])

def p_lista_identificadores(p):
    '''lista_identificadores : identificador
                             | identificador COMA lista_identificadores'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_instrucciones(p):
    '''instrucciones : instruccion
                     | instruccion instrucciones'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_instruccion(p):
    '''instruccion : READ identificador PUNTOYCOMA
                   | asignacion PUNTOYCOMA
                   | PRINTF PARIZQ CADENA PARDER PUNTOYCOMA
                   | bloque
                   | END PUNTOYCOMA'''
    p[0] = p[1:]

def p_asignacion(p):
    'asignacion : identificador IGUAL expresion'
    p[0] = ('asignacion', p[1], p[3])

def p_expresion(p):
    '''expresion : identificador
                 | NUMERO
                 | expresion MAS expresion'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('suma', p[1], p[3])

def p_bloque(p):
    '''bloque : LLAVEIZQ instrucciones LLAVEDER
              | LLAVEIZQ instrucciones END LLAVEDER'''  # Permitir bloques con END
    p[0] = ('bloque', p[2])  # Guardar las instrucciones en el bloque

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
