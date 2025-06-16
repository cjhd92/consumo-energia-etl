# scripts/extract.py
import pandas as pd
import os

def extract_data():
    url = "https://raw.githubusercontent.com/cjhd92/etl-csv-project/refs/heads/main/consumo_electrico.csv"
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "consumo_electrico.csv")

    print(f"Descargando datos desde: {url}")
    df = pd.read_csv(url)
    df.to_csv(output_path, index=False)
    print(f"Archivo guardado en: {output_path}")

if __name__ == "__main__":
    extract_data()
