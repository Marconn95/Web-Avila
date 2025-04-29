from flask import Flask, request, send_from_directory, render_template
import sqlite3
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Crear el archivo consultas.csv con encabezado si no existe
if not os.path.exists('consultas.csv'):
    with open('consultas.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['Cédula', 'Apellidos', 'Nombres', 'Curso', 'Fecha y Hora'])

# Función para buscar en la base de datos y registrar la consulta
def registrar_consulta(cedula_consultada):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT cedula, apellidos, nombres, curso_id
        FROM alumnos
        WHERE cedula = ?
    ''', (cedula_consultada,))
    
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('consultas.csv', mode='a', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow([*resultado, fecha_hora])
        return resultado
    else:
        return None
@app.route('/')
def index():
    return render_template('index.html')

PDF_FOLDER = os.path.join('static', 'pdfs')

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
    app.run(host='0.0.0.0', port=5000, debug=True)
