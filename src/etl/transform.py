# -*- coding: utf-8 -*-
import pandas as pd

def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    print("🧹 Iniciando transformación de datos...")

    # Estandarizar nombres de columnas
    df.columns = [col.strip().title() for col in df.columns]

    # Eliminar duplicados y registros vacíos
    df = df.drop_duplicates()
    df = df.dropna(subset=["Comentario"])

    # Rellenar valores faltantes
    df["Ciudad"] = df["Ciudad"].fillna("Desconocida")
    df["Nivel De Urgencia"] = df["Nivel De Urgencia"].fillna("Media")

    # Normalizar texto de comentarios
    df["Comentario"] = df["Comentario"].str.lower()

    # Crear una columna nueva: longitud del texto
    df["LongitudComentario"] = df["Comentario"].apply(len)

    # Eliminar espacios sobrantes
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    print(f"✅ Datos transformados: {df.shape[0]} filas listas.")
    return df
