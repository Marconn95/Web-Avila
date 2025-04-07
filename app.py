from flask import Flask, request, send_from_directory, render_template, abort
import os

app = Flask(__name__)
PDF_FOLDER = os.path.join('static', 'pdfs')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    cedula = request.form.get('cedula')
    archivo = f"{cedula}.pdf"
    ruta = os.path.join(PDF_FOLDER, archivo)

    if os.path.exists(ruta):
        return send_from_directory(PDF_FOLDER, archivo, as_attachment=True)
    else:
        return f"No se encontró el archivo para la cédula {cedula}", 404

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=5000, debug=True))