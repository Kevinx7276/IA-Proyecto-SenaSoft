# -*- coding: utf-8 -*-
import pandas as pd
import os

def extraer_datos(nombre_archivo="dataset_comunidades_senasoft.csv"):
    """
    Extrae los datos desde la carpeta /data y los carga en un DataFrame de Pandas.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "data", nombre_archivo)
    file_path = os.path.normpath(file_path)

    print(f"📥 Extrayendo datos desde: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"⚠️ No se encontró el archivo: {file_path}")

    df = pd.read_csv(file_path)
    print(f"✅ Datos extraídos: {df.shape[0]} filas y {df.shape[1]} columnas.")
    return df
