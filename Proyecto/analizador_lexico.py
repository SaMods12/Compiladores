import ply.lex as lex

# Palabras reservadas en Java
reservadas = {
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

# Lista de tokens incluyendo operadores y símbolos comunes en Java
tokens = [
    'DIGITO', 'PUNTO', 'PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO', 'LLAVE_ABIERTA', 'LLAVE_CERRADA',
    'PUNTO_Y_COMA', 'IDENTIFICADOR', 'IGUAL', 'OPERADOR_SUMA', 'OPERADOR_RESTA', 'OPERADOR_MULTIPLICACION',
    'OPERADOR_DIVISION','MAYOR_IGUAL', 'MENOR_IGUAL', 'MAS_MAS', 'COMA', 'CADENA'
] + list(reservadas.values())

# Expresiones regulares para los tokens
t_DIGITO = r'\d'
t_PUNTO = r'\.'
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_PUNTO_Y_COMA = r';'
t_IGUAL = r'='
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_MAS_MAS = r'\+\+'
t_OPERADOR_SUMA = r'\+'
t_OPERADOR_RESTA = r'-'
t_OPERADOR_MULTIPLICACION = r'\*'
t_OPERADOR_DIVISION = r'/'
t_CADENA = r'\".*?\"'
t_ignore = ' \t'

# Identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reservadas:
        t.type = reservadas[t.value]  # Palabra reservada
    else:
        t.type = 'IDENTIFICADOR'  # Identificador
    return t

# Manejo de nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Definir el token de error
def t_error(t):
    print('Caracter no válido', t.value[0])
    t.lexer.skip(1)

# Inicializar el lexer
lexer = lex.lex()

# Función para analizar el código
def analyze_code(text):
    lexer.input(text)
    
    resultado_lexico = []
    contador = {}
    
    # Analizar el texto línea por línea
    lines = text.splitlines()
    
    for i, line in enumerate(lines, start=1):
        lexer.input(line)
        for token in lexer:
            # Clasificar el token según su tipo
            if token.type in reservadas.values():
                category = 'Reservado'
            elif token.type in ['PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO', 'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'PUNTO_Y_COMA', 'COMA']:
                category = 'Delimitador'
            elif token.type in ['OPERADOR_SUMA', 'OPERADOR_RESTA', 'OPERADOR_MULTIPLICACION', 'OPERADOR_DIVISION', 'IGUAL', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'MAS_MAS', 'PUNTO']:
                category = 'Simbolo'
            elif token.type == 'DIGITO':
                category = 'Número'
            elif token.type == 'IDENTIFICADOR':
                category = 'Identificador'
            elif token.type == 'CADENA':
                category = 'Cadena'
            else:
                category = 'Desconocido'
            
            resultado_lexico.append({'token': category, 'lexema': token.value, 'linea': i})
            
            # Contar tokens por tipo
            if category in contador:
                contador[category] += 1
            else:
                contador[category] = 1

    return resultado_lexico, contador

