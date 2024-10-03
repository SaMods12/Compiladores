from flask import Flask, render_template, request
import analizador_lexico
import analizador_sintactico

app = Flask(__name__)

# Inicializa variables globales
resultado_lexema = []
resultado_sintactico = []
errores = []
token_count = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global resultado_lexema, resultado_sintactico, token_count  # Hacemos referencia a las variables globales
    resultado_lexico = None
    resultado_sintactico = None
    texto = ""

    if request.method == 'POST':
        texto = request.form['texto']
        resultado_lexico, token_count = analizador_lexico.analyze_code(texto)
        analizador_sintactico.prueba_sintactico(texto)
        resultado_sintactico = analizador_sintactico.resultado_sintactico

    return render_template('index.html', resultado_lexico=resultado_lexico, resultado_sintactico=resultado_sintactico, token_count=token_count, texto=texto)

# Ruta para limpiar los resultados
@app.route('/clear', methods=['POST'])
def clear():
    global resultado_lexema, resultado_sintactico, errores, token_count
    resultado_lexema.clear()  # Limpiar el resultado léxico
    resultado_sintactico.clear()  # Limpiar el resultado sintáctico
    errores.clear()  # Limpiar la lista de errores
    token_count.clear()  # Limpiar el contador de tokens
    return render_template('index.html', resultado_lexico=None, resultado_sintactico=None, token_count=None, texto="")

if __name__ == '__main__':
    app.run(debug=True)
