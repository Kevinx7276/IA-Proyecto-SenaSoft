# -*- coding: utf-8 -*-
import pandas as pd
import os

def extraer_datos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..","..", "data", "dataset_comunidades_senasoft.csv")

    print(f"📥 Extrayendo datos desde: {file_path}")
    df = pd.read_csv(file_path)
    print(f"✅ Datos extraídos: {df.shape[0]} filas.")
    return df
