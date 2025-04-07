import sqlite3

#Conectar a la base de datos (se crea si no existe)
conn= sqlite3.connect('alumnos.db')
cursor =conn.cursor()

#Eliminar la tabla _cursos si existe
cursor.execute('DROP TABLE IF EXISTS alumnos_cursos')

#Crear las tablas: alumnos y cursos
cursor.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
               cedula TEXT PRIMARY KEY,
               apellidos TEXT,
               nombres TEXXT,
               curso_id INTEGER,
               FOREIGN KEY (curso_id) REFERENCES cursos(id)
               );
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS cursos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre_curso TEXT
               );
               ''')

#Guardar cambios y cerrar la conexión
conn.commit()
conn.close()