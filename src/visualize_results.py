# -*- coding: utf-8 -*-
"""
Visualización de resultados para KELU IA Comunitaria (no bloqueante)
Autor: SENA / SENASoft 2025
"""

import matplotlib.pyplot as plt
import pandas as pd
import threading
import os

# ==============================================================
# 🎨 GRÁFICA 1: CATEGORÍAS
# ==============================================================

def graficar_categorias(df: pd.DataFrame):
    """
    Genera una gráfica de barras con la distribución de categorías.
    Se ejecuta en un hilo separado para no congelar la aplicación.
    """
    if df is None or df.empty:
        print("⚠️ No hay datos para graficar.")
        return

    if "Categorias" not in df.columns:
        print("⚠️ El DataFrame no contiene la columna 'Categorias'.")
        return

    def mostrar_grafica():
        conteo = df["Categorias"].value_counts()
        plt.figure(figsize=(8, 5))
        plt.bar(
            conteo.index,
            conteo.values,
            color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6b7280']
        )
        plt.title("Distribución de Categorías – KELU IA Comunitaria")
        plt.xlabel("Categorías")
        plt.ylabel("Número de reportes")
        plt.xticks(rotation=15)
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Guardar imagen y mostrar sin bloquear
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "grafico_categorias.png")
        plt.savefig(output_path)
        plt.show(block=False)
        print(f"📊 Gráfica de categorías guardada en: {output_path}")

    hilo = threading.Thread(target=mostrar_grafica)
    hilo.start()

# ==============================================================
# 🔥 GRÁFICA 2: NIVELES DE URGENCIA
# ==============================================================

def graficar_urgencias(df: pd.DataFrame):
    """
    Genera una gráfica circular con la proporción de niveles de urgencia.
    También se ejecuta en un hilo aparte.
    """
    if df is None or df.empty:
        print("⚠️ No hay datos para graficar urgencias.")
        return

    col_urg = None
    for col in ["NivelDeUrgencia", "Nivel De Urgencia"]:
        if col in df.columns:
            col_urg = col
            break

    if not col_urg:
        print("⚠️ No se encontró la columna de urgencia.")
        return

    def mostrar_grafica_urgencia():
        conteo = df[col_urg].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(
            conteo.values,
            labels=conteo.index,
            autopct="%1.1f%%",
            colors=["#ef4444", "#f59e0b", "#10b981"],
            startangle=140
        )
        plt.title("Distribución de Niveles de Urgencia – KELU IA")
        plt.tight_layout()

        # Guardar imagen y mostrar sin bloquear
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "grafico_urgencias.png")
        plt.savefig(output_path)
        plt.show(block=False)
        print(f"📊 Gráfica de urgencias guardada en: {output_path}")

    hilo = threading.Thread(target=mostrar_grafica_urgencia)
    hilo.start()

# ==============================================================
# 🧩 FUNCIÓN PRINCIPAL DE VISUALIZACIÓN
# ==============================================================

def mostrar_todas(df: pd.DataFrame):
    """
    Llama a todas las gráficas principales.
    Ideal para ejecutar después del ETL.
    """
    graficar_categorias(df)
    graficar_urgencias(df)
