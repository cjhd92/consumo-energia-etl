import pandas as pd
import mysql.connector
import os

def load_data():
    input_path = "data/processed/consumo_electrico_limpio.csv"

    df = pd.read_csv(input_path)

    # Conexión a MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "cesar"),
        database=os.getenv("DB_NAME", "airflowdb"),
        port=int(os.getenv("DB_PORT", 3306))
    )

    cursor = connection.cursor()

    # Crear tabla si no existe
    create_table_query = """
    CREATE TABLE IF NOT EXISTS consumo_energia (
        fecha DATE,
        region VARCHAR(50),
        consumo_mwh INT,
        temperatura_c INT,
        fuente_principal VARCHAR(50),
        precio_eur_mwh DECIMAL(6,2),
        pico_hora TIME
    );
    """
    cursor.execute(create_table_query)

    # Eliminar datos anteriores (opcional)
    cursor.execute("DELETE FROM consumo_energia")

    # Insertar datos fila por fila
    insert_query = """
    INSERT INTO consumo_energia (fecha, region, consumo_mwh, temperatura_c, fuente_principal, precio_eur_mwh, pico_hora)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            row["fecha"],
            row["region"],
            int(row["consumo_mwh"]),
            int(row["temperatura_c"]),
            row["fuente_principal"],
            float(row["precio_eur_mwh"]),
            row["pico_hora"] if isinstance(row["pico_hora"], str) else "00:00"
        )
        cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("Datos insertados exitosamente en MySQL.")

if __name__ == "__main__":
    load_data()
