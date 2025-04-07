import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('alumnos.db')
cursor = conn.cursor()

# Muestra las tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Verifica las columnas de la tabla alumnos
cursor.execute("PRAGMA table_info(alumnos);")
print(cursor.fetchall())

conn.close()