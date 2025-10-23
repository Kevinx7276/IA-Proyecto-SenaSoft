# -*- coding: utf-8 -*-
"""
KELU IA Comunitaria – Sistema MVC + ETL + IA + Vista Web + Evaluación del Modelo + Ética
Autor: SENA / SENASoft 2025
"""

import os
import sys
import time
import webbrowser
import threading
import requests
import pandas as pd
from dotenv import load_dotenv
from visualize_results import graficar_categorias
from evaluate_model import evaluar_modelo  # ✅ Evaluación del modelo
from ethics import evaluar_etica           # ✅ Módulo ético

# ==============================================================
# CONFIGURACIÓN INICIAL
# ==============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
load_dotenv()

print("🚀 Iniciando aplicación KELU IA Comunitaria...")

# ==============================================================
# IMPORTACIONES
# ==============================================================

from controllers.etl_controller import ejecutar_proceso_etl
from views.chat_view import app as chat_app

# ==============================================================
# CONFIGURACIÓN DE RED (IP LOCAL)
# ==============================================================

HOST = "192.168.0.122"  # Cambia según tu IP local (usa ipconfig)
PORT = 5000

# ==============================================================
# FUNCIÓN PARA LEVANTAR FLASK
# ==============================================================

def iniciar_servidor():
    print(f"🌐 Iniciando servidor Flask en http://{HOST}:{PORT} ...")
    chat_app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# ==============================================================
# FUNCIÓN PARA ESPERAR A QUE EL SERVIDOR ESTÉ LISTO
# ==============================================================

def esperar_servidor(url, intentos=20, pausa=1):
    for _ in range(intentos):
        try:
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(pausa)
    return False

# ==============================================================
# FLUJO PRINCIPAL
# ==============================================================

def main():
    print("\n==============================")
    print(" 🦅 KELU IA COMUNITARIA")
    print("==============================\n")

    # Paso 1️⃣: Ejecutar proceso ETL y capturar datos limpios
    df = ejecutar_proceso_etl(retornar_dataframe=True)

    # Paso 2️⃣: Evaluar el modelo de clasificación
    try:
        print("\n🔍 Evaluando rendimiento del modelo...")
        df_eval = df[['Categorias', 'Categoría Del Problema']].copy()
        df_eval.rename(columns={
            'Categorias': 'Categoria_Predicha',
            'Categoría Del Problema': 'Categoria_Real'
        }, inplace=True)

        # Ejecutar evaluación del modelo
        evaluar_modelo(df_eval)

        # Guardar resultados en archivo
        reporte_path = os.path.join(BASE_DIR, "..", "data", "reporte_clasificacion.txt")
        from sklearn.metrics import classification_report
        with open(reporte_path, "w", encoding="utf-8") as f:
            f.write("📊 Reporte de Clasificación – KELU IA Comunitaria\n\n")
            f.write(classification_report(df_eval["Categoria_Real"], df_eval["Categoria_Predicha"]))
        print(f"📄 Reporte guardado en: {reporte_path}")

    except Exception as e:
        print(f"⚠️ No se pudo evaluar el modelo: {e}")

    # Paso 3️⃣: Evaluación ética y detección de sesgos
    try:
        evaluar_etica(df)
    except Exception as e:
        print(f"⚠️ No se pudo realizar la evaluación ética: {e}")

    # Paso 4️⃣: Visualización de resultados
    try:
        graficar_categorias(df)
    except Exception as e:
        print(f"⚠️ No se pudo graficar categorías: {e}")

    # Paso 5️⃣: Iniciar el servidor Flask en un hilo
    servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    servidor.start()

    # Paso 6️⃣: Esperar hasta que el servidor esté accesible
    url = f"http://{HOST}:{PORT}"
    print(f"⌛ Esperando a que el servidor esté disponible en {url} ...")
    if esperar_servidor(url):
        print("✅ Servidor activo, abriendo navegador...")
        webbrowser.open(url)
    else:
        print("⚠️ No se pudo conectar automáticamente. Ábrelo manualmente en:", url)

    # Mantener la aplicación viva
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido manualmente.")


if __name__ == "__main__":
    main()
