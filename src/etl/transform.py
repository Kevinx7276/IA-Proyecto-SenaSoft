# -*- coding: utf-8 -*-
"""
Módulo de Transformación de Datos – KELU IA Comunitaria
Autor: SENA / SENASoft 2025

Procesos:
✅ Limpieza y normalización de datos.
✅ Clasificación automática (Educación, Salud, Medio Ambiente, Seguridad, Otro).
✅ Generación de explicación (columna 'Razon').
✅ Eliminación de duplicados, conservando diferencias de urgencia.
"""

import pandas as pd

def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    print("🧹 Iniciando transformación de datos reales...")

    # ====================================================
    # 1️⃣ Validación inicial
    # ====================================================
    if df is None or df.empty:
        print("⚠️ DataFrame vacío. No hay datos para transformar.")
        return pd.DataFrame()

    # ====================================================
    # 2️⃣ Normalización de nombres de columnas
    # ====================================================
    df.columns = [col.strip().title() for col in df.columns]

    # ====================================================
    # 3️⃣ Verificación de columnas mínimas necesarias
    # ====================================================
    columnas_requeridas = ["Comentario", "Ciudad", "Nivel De Urgencia", "Categoría Del Problema"]
    for col in columnas_requeridas:
        if col not in df.columns:
            print(f"⚠️ Columna faltante: {col}. Se creará vacía.")
            df[col] = ""

    # ====================================================
    # 4️⃣ Limpieza básica de texto y valores faltantes
    # ====================================================
    df = df.dropna(subset=["Comentario"])
    df["Comentario"] = df["Comentario"].astype(str).str.lower().str.strip()
    df["Ciudad"] = df["Ciudad"].fillna("Desconocida").astype(str).str.lower().str.strip()
    df["Nivel De Urgencia"] = df["Nivel De Urgencia"].fillna("Media").astype(str).str.strip()

    # ====================================================
    # 5️⃣ Longitud del comentario (métrica de análisis)
    # ====================================================
    df["LongitudComentario"] = df["Comentario"].apply(len)

    # ====================================================
    # 6️⃣ Clasificación automática + explicación
    # ====================================================
    def clasificar_y_explicar(texto, categoria_existente):
        texto_l = texto.lower()
        razon = ""

        # Palabras clave para detección
        if any(pal in texto_l for pal in ["escuela", "profesor", "colegio", "educación", "estudiante", "clases"]):
            categoria_detectada = "Educación"
            razon = "Palabras clave detectadas: escuela, profesor, clases"
        elif any(pal in texto_l for pal in ["hospital", "salud", "médico", "vacuna", "enfermo", "eps", "cita"]):
            categoria_detectada = "Salud"
            razon = "Palabras clave detectadas: salud, hospital, médico"
        elif any(pal in texto_l for pal in ["basura", "río", "contaminación", "árbol", "limpieza", "reciclaje", "ambiente"]):
            categoria_detectada = "Medio Ambiente"
            razon = "Palabras clave detectadas: basura, río, contaminación"
        elif any(pal in texto_l for pal in ["robo", "violencia", "seguridad", "policía", "arma", "asalto"]):
            categoria_detectada = "Seguridad"
            razon = "Palabras clave detectadas: robo, policía, seguridad"
        else:
            categoria_detectada = "Otro"
            razon = "Sin coincidencias claras – clasificado como 'Otro'"

        # Comparar con categoría original del dataset
        if categoria_existente and categoria_existente.strip().lower() not in ["", "nan", "otro"]:
            categoria_existente = categoria_existente.title()
            if categoria_existente == categoria_detectada:
                razon = f"Confirmado por texto: {razon}"
            else:
                razon = f"Texto indica '{categoria_detectada.lower()}', pero dataset tenía '{categoria_existente.lower()}'"
                # Mantiene la categoría original para no sobreescribir
                categoria_detectada = categoria_existente

        return (categoria_detectada, razon)

    # Aplicar clasificación
    df[["Categorias", "Razon"]] = df.apply(
        lambda row: pd.Series(
            clasificar_y_explicar(row["Comentario"], row.get("Categoría Del Problema", ""))
        ),
        axis=1
    )

    # ====================================================
    # 7️⃣ Eliminación de duplicados inteligentes
    # ====================================================
    before = len(df)
    df = df.drop_duplicates(subset=["Comentario", "Ciudad", "Categorias"], keep="first")
    after = len(df)
    print(f"🧹 Registros duplicados eliminados: {before - after}")

    # ====================================================
    # 8️⃣ Renombrar columnas para consistencia con MySQL
    # ====================================================
    df = df.rename(columns={"Nivel De Urgencia": "NivelDeUrgencia"})

    # ====================================================
    # 9️⃣ Resumen final
    # ====================================================
    print("✅ Datos transformados correctamente.")
    print(f"📊 Total registros finales: {len(df)}")
    print("🧩 Columnas finales:", list(df.columns))

    return df
