import pandas as pd
import os



def transform_data():
    input_path = "data/raw/consumo_electrico.csv"
    output_dir = "data/processed/"


    output_path = os.path.join(output_dir + "consumo_electrico_limpio.csv")
    os.makedirs(output_dir,exist_ok= tuple)

    df = pd.read_csv(input_path)   #Leer el archivo original

    # *** Procedimiento para la limpieza y el transformacion de los datos ***

    df['fecha'] = pd.to_datetime(df['fecha'],errors= 'coerce')  #Convertir la columna fecha a datetime

    df.dropna(subset=["fecha", "region", "consumo_mwh", "precio_eur_mwh"],inplace= True)   #Eliminar filas con valores faltantes(NaN) en algunas de las columnas

    df['region'] = df['region'].str.strip()   #Eliminar espacio
    df['region'] = df['region'].str.title()   #Capitalizar

    df['consumo_mwh'] = pd.to_numeric(df['consumo_mwh'],errors='coerce')
    df['temperatura_c'] = pd.to_numeric(df['temperatura_c'],errors='coerce')
    df['precio_eur_mwh'] = pd.to_numeric(df['precio_eur_mwh'],errors='coerce')

    df.dropna(subset=["fecha", "region", "consumo_mwh","temperatura_c", "precio_eur_mwh"],inplace= True)   #Eliminar filas con valores faltantes(NaN) en algunas de las columnas

    df = df[df['consumo_mwh'] > 0]     #MAntiene los datos que superen el valor de 0 en esta columna
    df = df[df['precio_eur_mwh'] > 0]  #MAntiene los datos que superen el valor de 0 en esta columna

    df.reset_index(drop=True,inplace=True)   #resetea los index 


    df.to_csv(output_path, index=False)
    print(f"Datos limpios guardados en: {output_path}")


    

if __name__ == "__main__":
    transform_data()