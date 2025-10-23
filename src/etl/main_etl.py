# -*- coding: utf-8 -*-
"""
main_etl.py — Ejecutor principal del proceso ETL (Águila IA Comunitaria)
Autor: SENA / SENASoft 2025
"""

from extract import extraer_datos
from transform import transformar_datos
from models.data_model import DataModel  # usamos la clase DataModel

def main():
    print("🚀 Iniciando proceso ETL del proyecto SENA...")

    # 1️⃣ Extraer datos del CSV
    datos_crudos = extraer_datos()

    # 2️⃣ Transformar datos (limpieza, clasificación y explicación)
    datos_limpios = transformar_datos(datos_crudos)

    # 3️⃣ Cargar datos usando el modelo DataModel
    modelo = DataModel()
    modelo.guardar_datos(datos_limpios)
    modelo.cerrar_conexion()

    print("✅ ETL completado correctamente.")

if __name__ == "__main__":
    main()
