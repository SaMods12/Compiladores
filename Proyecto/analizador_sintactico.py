from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc

# Configuración de la aplicación Flask
app = Flask(__name__)

# Variables globales para almacenar resultados
resultado_lexema = []
resultado_sintactico = []
errores = []
token_count = {}

# Palabras reservadas
reservada = {
    'if': 'IF', 
    'else': 'ELSE', 
    'while': 'WHILE', 
    'for': 'FOR', 
    'int': 'INT', 
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

# Reglas gramaticales para un bucle for
def p_instruccion_for(p):
    '''instruccion : FOR PARIZQ INT identificador IGUAL NUMERO PUNTOYCOMA identificador MENORIGUAL NUMERO PUNTOYCOMA identificador MASMAS PARDER bloque'''
    p[0] = ('for', ('declaracion', p[3], p[4], p[6]), ('condicion', p[8], p[9]), ('incremento', p[11]), p[14])

# Bloque de instrucciones dentro del bucle for
def p_bloque(p):
    '''bloque : LLAVEIZQ instruccion_llamada LLAVEDER'''
    p[0] = ('bloque', p[2])

# Llamada a System.out.println
def p_instruccion_llamada(p):
    '''instruccion_llamada : SYSTEM PUNTO OUT PUNTO PRINTLN PARIZQ CADENA MAS identificador PARDER PUNTOYCOMA'''
    p[0] = ('println', p[7], p[9])

# Error de sintaxis
def p_error(p):
    if p:
        errores.append(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        errores.append("Error de sintaxis en la entrada")

# Función para el análisis sintáctico
def prueba_sintactico(data):
    global resultado_sintactico, errores
    resultado_sintactico.clear()  # Limpiar el resultado antes de cada prueba
    errores.clear()  # Limpiar la lista de errores
    parser = yacc.yacc()
    parser.parse(data)
    if errores:
        resultado_sintactico.extend(errores)
    else:
        resultado_sintactico.append("Análisis sintáctico correcto")

# Ruta principal con el formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    texto = ""
    if request.method == 'POST':
        # Obtener los datos del formulario
        texto = request.form['texto']
        prueba_lexico(texto)  # Ejecutar el análisis léxico
        prueba_sintactico(texto)  # Ejecutar el análisis sintáctico
        return render_template('index.html', resultado_lexema=resultado_lexema, 
                               resultado_sintactico=resultado_sintactico, 
                               token_count=token_count, texto=texto)
    return render_template('index.html', resultado_lexema=None, resultado_sintactico=None, token_count=None, texto=texto)

# Ruta para limpiar los resultados
@app.route('/clear', methods=['POST'])
def clear():
    global resultado_lexema, resultado_sintactico, errores, token_count
    resultado_lexema.clear()  # Limpiar el resultado léxico
    resultado_sintactico.clear()  # Limpiar el resultado sintáctico
    errores.clear()  # Limpiar la lista de errores
    token_count.clear()  # Limpiar el contador de tokens
    return render_template('index.html', resultado_lexema=None, resultado_sintactico=None, token_count=None, texto="")

# Ejecución de la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)