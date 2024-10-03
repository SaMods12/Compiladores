from flask import Flask, render_template, request
import analizador_lexico
import analizador_sintactico

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_lexico = None
    resultado_sintactico = None
    token_count = {}  # Inicializa token_count como un diccionario vacío
    texto = ""

    if request.method == 'POST':
        texto = request.form['texto']
        resultado_lexico, token_count = analizador_lexico.analyze_code(texto)  # Cambia esto para capturar el contador
        analizador_sintactico.prueba_sintactico(texto)
        resultado_sintactico = analizador_sintactico.resultado_sintactico

    return render_template('index.html', resultado_lexico=resultado_lexico, resultado_sintactico=resultado_sintactico, token_count=token_count, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
