from flask import Flask, render_template, request
import analizador_lexico
import analizador_sintactico
import re

app = Flask(__name__)


# Lista ampliada de palabras prohibidas
PALABRAS_PROHIBIDAS = [
    "BACA", "BAKA", "BAKA", "BUEY", "CACA", "CAKA", "CAGA", "CAGO", "CAKA", "CAKO",
    "COGE", "COJA", "COJE", "COJI", "COJO", "COLA", "CULO", "FETO", "FETO", "GUEY",
    "JOTO", "KAKA", "KAGO", "KOJO", "KULO", "MAME", "MAMO", "MEAR", "MEON", "MIAR",
    "MOCO", "MULA", "PEDA", "PEDO", "PENE", "PUTA", "PUTO", "QULO", "RATA", "RUIN",
    "TETA", "VACA", "VAKA", "VAGO", "VAKA", "VIEJ", "VIEJ", "WUEY"
]

def limpiar_nombre(nombre):
    return nombre.replace("Ñ", "X").upper()

def verificar_curp(curp):
    for palabra in PALABRAS_PROHIBIDAS:
        if curp.startswith(palabra):
            return True
    return False

def generar_curp(nombre, primer_apellido, segundo_apellido, dia_nacimiento, mes_nacimiento, anio_nacimiento, sexo, estado):
    nombre = limpiar_nombre(nombre)
    primer_apellido = limpiar_nombre(primer_apellido)
    segundo_apellido = limpiar_nombre(segundo_apellido)
    
    primera_letra_apellido = primer_apellido[0].upper()
    primera_vocal_apellido = re.search(r'[AEIOU]', primer_apellido[1:], re.I)
    primera_vocal_apellido = primera_vocal_apellido.group(0).upper() if primera_vocal_apellido else 'X'
    primera_letra_segundo_apellido = segundo_apellido[0].upper() if segundo_apellido else 'X'
    primera_letra_nombre = nombre[0].upper()

    # Obtener consonantes adicionales
    consonante_segundo_apellido = re.search(r'[^AEIOU]', segundo_apellido[1:], re.I)
    consonante_nombre = re.search(r'[^AEIOU]', nombre[1:], re.I)
    
    consonante_segundo_apellido = consonante_segundo_apellido.group(0).upper() if consonante_segundo_apellido else 'X'
    consonante_nombre = consonante_nombre.group(0).upper() if consonante_nombre else 'X'

    anio = anio_nacimiento[-2:]
    mes = mes_nacimiento.zfill(2)
    dia = dia_nacimiento.zfill(2)
    genero = sexo.upper()
    estado = estado.upper()

    consonantes_internas = ''.join(
        (re.search(r'[^AEIOU]', x[1:], re.I).group(0).upper() if re.search(r'[^AEIOU]', x[1:], re.I) else 'X')
        for x in (primer_apellido, segundo_apellido, nombre)
    )

    homoclave = 'XX'
    
    # Formar CURP provisional
    curp = (
        f"{primera_letra_apellido}{primera_vocal_apellido}"
        f"{consonante_segundo_apellido}{primera_letra_nombre}"
        f"{anio}{mes}{dia}{genero}{estado}{consonantes_internas}{homoclave}"
    )

    if verificar_curp(curp):
        curp = (
            f"{primera_letra_apellido}X"
            f"{consonante_segundo_apellido}{primera_letra_nombre}"
            f"{anio}{mes}{dia}{genero}{estado}{consonantes_internas}{homoclave}"
        )
    
    return curp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    nombre = request.form.get('nombre')
    primer_apellido = request.form.get('primer_apellido')
    segundo_apellido = request.form.get('segundo_apellido')
    dia_nacimiento = request.form.get('dia_nacimiento')
    mes_nacimiento = request.form.get('mes_nacimiento')
    anio_nacimiento = request.form.get('anio_nacimiento')
    sexo = request.form.get('sexo')
    estado = request.form.get('estado')
    
    curp = generar_curp(
        nombre, primer_apellido, segundo_apellido,
        dia_nacimiento, mes_nacimiento, anio_nacimiento,
        sexo, estado
    )
    
    return f"CURP generada: {curp}"


if __name__ == '__main__':
    app.run(debug=True)
