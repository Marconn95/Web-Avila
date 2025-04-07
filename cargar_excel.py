import sqlite3
import pandas as pd

# Función para crear las tablas en la base de datos
def crear_tablas():
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()

    # Crear tabla de cursos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_curso TEXT
    );
    ''')

    # Crear tabla de alumnos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        cedula TEXT PRIMARY KEY,
        apellidos TEXT,
        nombres TEXT,
        curso_id INTEGER,
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
    );
    ''')

    conn.commit()
    conn.close()

# Función para cargar los cursos desde el archivo Excel
def cargar_cursos(df_cursos):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()

    # Insertar cursos en la base de datos
    for _, row in df_cursos.iterrows():
        cursor.execute('''
        INSERT INTO cursos (nombre_curso) VALUES (?)
        ''', (row['nombre_curso'],))

    conn.commit()
    conn.close()

# Función para cargar los alumnos desde el archivo Excel
def cargar_alumnos(df_alumnos):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()

    # Insertar alumnos en la base de datos
    for _, row in df_alumnos.iterrows():
        # Obtener el id del curso
        cursor.execute('''
        SELECT id FROM cursos WHERE nombre_curso = ?
        ''', (row['curso'],))
        curso_id = cursor.fetchone()
        
        if curso_id:
            cursor.execute('''
            INSERT INTO alumnos (cedula, apellidos, nombres, curso_id) 
            VALUES (?, ?, ?, ?)
            ''', (row['cedula'], row['apellidos'], row['nombres'], curso_id[0]))

    conn.commit()
    conn.close()

# Función principal que carga el Excel y lo procesa
def cargar_datos_desde_excel(ruta_excel):
    # Leer las hojas del archivo Excel
    df_cursos = pd.read_excel(ruta_excel, sheet_name='cursos')
    df_alumnos = pd.read_excel(ruta_excel, sheet_name='alumnos')

    # Crear las tablas si no existen
    crear_tablas()

    # Cargar los cursos y alumnos a la base de datos
    cargar_cursos(df_cursos)
    cargar_alumnos(df_alumnos)

# Ejecutar el proceso
ruta_excel = 'base_alumnos.xlsx'  # Cambia esto por la ruta de tu archivo Excel
cargar_datos_desde_excel(ruta_excel)
