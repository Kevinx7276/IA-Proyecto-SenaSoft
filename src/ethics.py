# -*- coding: utf-8 -*-
"""
Módulo de Ética y Transparencia – Águila IA Comunitaria
Define principios de uso ético, explicabilidad y manejo responsable de datos.
"""

def evaluar_etica(df):
    print("\n🧭 Evaluación Ética del Modelo")

    # 1️⃣ Revisión de datos sensibles
    columnas_sensibles = [col for col in df.columns if "nombre" in col.lower() or "id" in col.lower()]
    if columnas_sensibles:
        print(f"⚠️ Se encontraron posibles datos personales: {columnas_sensibles}")
    else:
        print("✅ No se detectaron columnas con datos personales.")

    # 2️⃣ Análisis de balance de categorías
    balance = df['Categorias'].value_counts(normalize=True) * 100
    print("\n📊 Distribución de categorías (porcentaje):")
    print(balance)

    if balance.max() > 70:
        print("⚠️ Posible sesgo: una categoría domina los datos.")
    else:
        print("✅ Distribución de categorías equilibrada.")

    print("\n🧠 Transparencia: El sistema Águila IA explica sus decisiones de clasificación "
          "indicando las palabras clave y contexto que motivaron su predicción.\n")
