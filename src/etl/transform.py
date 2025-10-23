# -*- coding: utf-8 -*-
import pandas as pd

def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia, normaliza y prepara los datos del dataset comunitario.
    Usa la columna 'Categoría del problema' si está disponible, 
    o infiere la categoría y la razón según palabras clave.
    """
    print("🧹 Iniciando transformación de datos reales...")

    # ============================================================
    # 🔍 Validación inicial
    # ============================================================
    if df is None or df.empty:
        print("⚠️ DataFrame vacío. No hay datos para transformar.")
        return pd.DataFrame()

    # ============================================================
    # 🧾 Normalizar nombres de columnas
    # ============================================================
    df.columns = [col.strip().title() for col in df.columns]

    # ============================================================
    # 🧩 Asegurar columnas clave
    # ============================================================
    columnas_requeridas = ["Comentario", "Ciudad", "Nivel De Urgencia", "Categoría Del Problema"]
    for col in columnas_requeridas:
        if col not in df.columns:
            print(f"⚠️ Columna faltante: {col}. Se creará vacía.")
            df[col] = ""

    # ============================================================
    # 🧹 Limpieza básica
    # ============================================================
    df = df.drop_duplicates()
    df = df.dropna(subset=["Comentario"])
    df["Comentario"] = df["Comentario"].astype(str).str.lower().str.strip()

    # ============================================================
    # 🌎 Normalizar columnas de texto
    # ============================================================
    df["Ciudad"] = df["Ciudad"].fillna("Desconocida").astype(str).str.strip()

    # Manejo flexible del campo de urgencia (con o sin espacio)
    if "Nivel De Urgencia" in df.columns:
        df["NivelDeUrgencia"] = df["Nivel De Urgencia"].fillna("Media").astype(str).str.strip()
    else:
        df["NivelDeUrgencia"] = df.get("NivelDeUrgencia", "Media").astype(str).str.strip()

    # ============================================================
    # 🏷️ Normalizar categorías si existen
    # ============================================================
    if "Categoría Del Problema" in df.columns:
        df["Categoría Del Problema"] = (
            df["Categoría Del Problema"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # ============================================================
    # 🧮 Métrica adicional: longitud del comentario
    # ============================================================
    df["LongitudComentario"] = df["Comentario"].apply(len)

    # ============================================================
    # 🤖 Clasificación automática + explicación
    # ============================================================
    def clasificar_y_explicar(texto, categoria_existente):
        texto_l = texto.lower()

        # Si la categoría ya está definida, respetarla
        if categoria_existente and categoria_existente.strip().lower() not in ["", "nan", "otro"]:
            return (categoria_existente.title(), f"Categoría original del dataset: {categoria_existente}")

        # Inferencia por palabras clave
        if any(pal in texto_l for pal in ["escuela", "profesor", "colegio", "educación", "estudiante", "clases"]):
            return ("Educación", "Palabras clave detectadas: escuela, profesor, clases")
        elif any(pal in texto_l for pal in ["hospital", "salud", "médico", "vacuna", "enfermo", "eps"]):
            return ("Salud", "Palabras clave detectadas: salud, hospital, médico")
        elif any(pal in texto_l for pal in ["basura", "río", "contaminación", "árbol", "limpieza", "reciclaje"]):
            return ("Medio Ambiente", "Palabras clave detectadas: basura, río, contaminación")
        elif any(pal in texto_l for pal in ["robo", "violencia", "seguridad", "policía", "arma"]):
            return ("Seguridad", "Palabras clave detectadas: robo, policía, seguridad")
        else:
            return ("Otro", "Sin coincidencias claras – clasificado como 'Otro'")

    df[["Categorias", "Razon"]] = df.apply(
        lambda row: pd.Series(clasificar_y_explicar(row["Comentario"], row.get("Categoría Del Problema", ""))),
        axis=1
    )

    # ============================================================
    # 📊 Resumen final
    # ============================================================
    resumen = df["Categorias"].value_counts().to_dict()
    print(f"✅ Datos transformados correctamente ({len(df)} registros).")
    print("📊 Distribución de categorías:", resumen)
    print("🧩 Columnas finales:", list(df.columns))

    return df
