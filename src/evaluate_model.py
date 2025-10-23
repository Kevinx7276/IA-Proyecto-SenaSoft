# -*- coding: utf-8 -*-
"""
Módulo de Evaluación de Clasificación – KELU IA Comunitaria
Evalúa la precisión del modelo y genera un reporte en /data/reporte_clasificacion.txt sin bloquear la app.
"""

import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

def evaluar_modelo(df: pd.DataFrame, save_path=None):
    """
    Evalúa el modelo de clasificación comparando categorías reales vs predichas.
    Genera reporte .txt y guarda la matriz de confusión como imagen.
    No abre gráficos interactivos.
    """

    if 'Categoria_Real' not in df.columns or 'Categoria_Predicha' not in df.columns:
        print("⚠️ Faltan columnas requeridas: 'Categoria_Real' o 'Categoria_Predicha'")
        return

    print("\n📊 Evaluando rendimiento del modelo...")

    # --- Generar métricas ---
    reporte = classification_report(df['Categoria_Real'], df['Categoria_Predicha'])
    print(reporte)

    # --- Guardar reporte en TXT ---
    if not save_path:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, '..', 'data', 'reporte_clasificacion.txt')

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("📊 Reporte de Clasificación – KELU IA Comunitaria\n\n")
        f.write(reporte)

    print(f"📄 Reporte guardado correctamente en: {save_path}")

    # --- Crear matriz de confusión ---
    categorias = sorted(df['Categoria_Real'].unique())
    cm = confusion_matrix(df['Categoria_Real'], df['Categoria_Predicha'], labels=categorias)

    plt.figure(figsize=(7, 5))
    plt.imshow(cm, interpolation='nearest', cmap='Blues')
    plt.title("Matriz de Confusión – KELU IA Comunitaria")
    plt.colorbar()

    plt.xticks(range(len(categorias)), categorias, rotation=45, ha="right")
    plt.yticks(range(len(categorias)), categorias)

    # Añadir números dentro de las celdas
    for i in range(len(categorias)):
        for j in range(len(categorias)):
            plt.text(j, i, cm[i, j], ha="center", va="center", color="black")

    plt.xlabel("Predicha")
    plt.ylabel("Real")
    plt.tight_layout()

    # --- Guardar imagen en lugar de mostrarla ---
    img_path = os.path.join(os.path.dirname(save_path), 'matriz_confusion.png')
    plt.savefig(img_path, dpi=300)
    plt.close()

    print(f"📊 Matriz de confusión guardada en: {img_path}")
