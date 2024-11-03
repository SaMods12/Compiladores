import ply.yacc as yacc
from analizador_lexico import tokens

# Reglas sintácticas para CURP
def p_curp(p):
    '''curp : APELLIDO APELLIDO NOMBRE FECHA_CORTA SEXO ENTIDAD CONSONANTE_INTERNA CONSONANTE_INTERNA CONSONANTE_INTERNA'''
    # Construcción de la CURP a partir de los componentes
    p[0] = ''.join(p[1:])

def p_error(p):
    if p:
        print("Error de sintaxis: Se encontró '%s' en la posición %d" % (p.value, p.lexpos))
    else:
        print("Error de sintaxis: Fin de entrada inesperado")

# Construir el parser
parser = yacc.yacc()

if __name__ == '__main__':
  
    result = parser.parse()
   
