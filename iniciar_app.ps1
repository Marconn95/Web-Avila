# Ruta al ejecutable de Python (ajustala si es necesario)
$pythonPath = "C:\Users\Usuario\AppData\Local\Programs\Python\Python311\python.exe"

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..."
    & $pythonPath -m venv venv
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..."
. .\venv\Scripts\Activate.ps1

# Instalar Flask si no está instalado
if (-not (pip show flask)) {
    Write-Host "Instalando Flask..."
    pip install flask
}

# Ejecutar la app
Write-Host "Iniciando la aplicación..."
python app.py
