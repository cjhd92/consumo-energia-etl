import pandas as pd
import os
import duckdb



def load_to_duckdb():

    input_path = "data/processed/consumo_electrico_limpio.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Archivo no encontrado: {input_path}")
    
    # Cargar CSV limpio en un DataFrame
    df = pd.read_csv(input_path)

    # Conectarse (o crear si no existe) a base de datos local DuckDB
    db_path = "data/consumo.duckdb"
    con = duckdb.connect(database=db_path)

    # Crear tabla nueva o sobrescribir
    con.execute("DROP TABLE IF EXISTS consumo_energia")

    # Crear tabla desde el DataFrame directamente
    con.execute("""
        CREATE TABLE consumo_energia AS SELECT * FROM df
    """)

    con.close()
    print(f"Datos cargados exitosamente en: {db_path}")

    

if __name__ == "__main__":
    load_to_duckdb()