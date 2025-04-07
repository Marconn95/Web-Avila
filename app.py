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

    # Aquí la consulta solo toma los datos de la tabla "alumnos"
    cursor.execute('''
        SELECT alumnos.cedula, alumnos.apellido, alumnos.nombre, alumnos.curso_id
        FROM alumnos
        WHERE alumnos.cedula = ?
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

@app.route('/', methods=['GET', 'POST'])
def buscar():
    mensaje = ''
    if request.method == 'POST':
        cedula = request.form['cedula'].strip()
        resultado = registrar_consulta(cedula)

        archivo_pdf = f'{cedula}.pdf'
        ruta_pdf = os.path.join('pdfs', archivo_pdf)

        if resultado and os.path.exists(ruta_pdf):
            return send_from_directory('pdfs', archivo_pdf, as_attachment=True)
        else:
            mensaje = 'Cédula no encontrada o archivo PDF no disponible.'
    
    return render_template('index.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
