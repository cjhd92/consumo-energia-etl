@echo off
echo ⚙️ Iniciando ejecución del proyecto ETL...

REM Crear entorno virtual si no existe
IF NOT EXIST venv (
    echo 🐍 Creando entorno virtual...
    python -m consumo_energetico venv
)

REM Activar entorno virtual
call consumo_energetico\Scripts\activate

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Ejecutar el dashboard de Streamlit
echo 🚀 Ejecutando aplicación...
streamlit run dashboard/dashboard.py

pause
