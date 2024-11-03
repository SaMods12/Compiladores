import ply.lex as lex

# Definición de los tokens
tokens = (
    'APELLIDO',
    'NOMBRE',
    'FECHA_CORTA',
    'SEXO',
    'ENTIDAD',
    'CONSONANTE_INTERNA',
    'HOMOCLAVE',
    'DIGITO_VERIFICADOR'  # Agregar un token para el dígito verificador
)

# Reglas de los tokens
t_APELLIDO = r'[A-ZÑ]{2}'         # Primeras dos letras del apellido
t_NOMBRE = r'[A-ZÑ]'               # Primera letra del nombre
t_FECHA_CORTA = r'\d{6}'           # Fecha en formato AAMMDD
t_SEXO = r'[HM]'                   # H para hombre, M para mujer
t_ENTIDAD = r'[A-Z]{2}'            # Clave de la entidad
t_CONSONANTE_INTERNA = r'[A-ZÑ]{3}'# Consonantes internas de apellidos y nombre
t_HOMOCLAVE = r'[A-Z0-9]{2}'       # Homoclave, formada por letras y números
t_DIGITO_VERIFICADOR = r'\d'       # Dígito verificador final

# Ignorar espacios y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print(f"Error de lexing en '{t.value}' en la posición {t.lexpos}")
    t.lexer.skip(1)

# Construir el lexer
def build_lexer():
    return lex.lex()

# Ejemplo de prueba del analizador léxico
if __name__ == '__main__':
    lexer = build_lexer()
    
    
    # Proceso de tokenización
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
