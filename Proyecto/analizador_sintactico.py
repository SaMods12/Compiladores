import ply.lex as lex
import ply.yacc as yacc

# Variables globales para almacenar resultados
resultado_lexema = []
resultado_sintactico = []
errores = []
token_count = {}

# Listas para llevar control de variables declaradas y leídas
variables_declaradas = set()
variables_leidas = set()

# Palabras reservadas
reservada = {
    'include': 'INCLUDE',
    'using': 'USING',
    'namespace': 'NAMESPACE',
    'std': 'STD',
    'int': 'INT',
    'main': 'MAIN',
    'return': 'RETURN',
    'cout': 'COUT'
}

# Lista completa de tokens
tokens = list(reservada.values()) + [
    'MENORQUE', 'MAYORQUE', 'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER', 
    'PUNTOYCOMA', 'DOBLEMENORQUE', 'CADENA', 'NUMERO', 'IOSTREAM'  # Añadir IOSTREAM
]

# Expresiones regulares para tokens simples
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PUNTOYCOMA = r';'
t_DOBLEMENORQUE = r'<<'

# Definición de tokens para tipos específicos
t_CADENA = r'\".*?\"'
t_NUMERO = r'\d+'
t_IOSTREAM = r'iostream'  # Definimos IOSTREAM

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Ignorar comentarios de una sola línea
def t_COMENTARIO_LINEA(t):
    r'//.*'
    pass  # Ignorar el comentario

# Ignorar comentarios de múltiples líneas
def t_COMENTARIO_MULTILINEA(t):
    r'/\*.*?\*/'
    pass  # Ignorar el comentario

# Manejo de errores en caracteres ilegales
def t_error(t):
    errores.append(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)  # Saltar el carácter ilegal

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

# Reglas gramaticales para instrucción imprimir en C++
# Definir la producción principal del programa
def p_programa(p):
    '''programa : include_statement using_statement main_function'''

# Producción para la inclusión de librerías
def p_include_statement(p):
    '''include_statement : INCLUDE MENORQUE IOSTREAM MAYORQUE'''

# Producción para la declaración del espacio de nombres (namespace)
def p_using_statement(p):
    '''using_statement : USING NAMESPACE STD PUNTOYCOMA'''

# Producción para la función `main`
def p_main_function(p):
    '''main_function : INT MAIN PARIZQ PARDER LLAVEIZQ statements LLAVEDER'''

# Producción para las declaraciones dentro de `main`
def p_statements(p):
    '''statements : statement statements
                  | statement'''

# Producción para cada declaración dentro de `main`
def p_statement(p):
    '''statement : cout_statement
                 | return_statement'''

# Producción para la instrucción `cout`
def p_cout_statement(p):
    '''cout_statement : COUT DOBLEMENORQUE CADENA PUNTOYCOMA'''

# Producción para la instrucción `return`
def p_return_statement(p):
    '''return_statement : RETURN NUMERO PUNTOYCOMA'''

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        errores.append(f"Error de sintaxis '{p.value}' en la línea {p.lineno}")
    else:
        errores.append("Error de sintaxis: entrada incompleta o incorrecta")

# Función para el análisis sintáctico
def prueba_sintactico(data):
    global resultado_sintactico, errores, variables_declaradas, variables_leidas
    resultado_sintactico.clear()  # Limpiar el resultado antes de cada prueba
    errores.clear()  # Limpiar la lista de errores
    variables_declaradas.clear()  # Limpiar variables declaradas
    variables_leidas.clear()  # Limpiar variables leídas
    parser = yacc.yacc()
    parser.parse(data, lexer=lex.lex())
    if errores:
        resultado_sintactico.extend(errores)
    else:
        resultado_sintactico.append("Análisis sintáctico correcto")
