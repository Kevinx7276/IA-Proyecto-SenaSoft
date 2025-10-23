# -*- coding: utf-8 -*-
"""
Controlador ETL – KELU IA Comunitaria
Autor: SENA / SENASoft 2025
"""
# -*- coding: utf-8 -*-
"""
Controlador ETL – KELU IA Comunitaria
Autor: SENA / SENASoft 2025
"""

import sys
import os

# Añadimos la carpeta padre (src/) al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.data_model import DataModel
from etl.extract import extraer_datos
from etl.transform import transformar_datos


def ejecutar_proceso_etl(retornar_dataframe=False):
    """
    Ejecuta el flujo completo del proceso ETL:
    1️⃣ Extrae datos desde el CSV
    2️⃣ Transforma (limpieza, clasificación, explicación)
    3️⃣ Carga los datos en MySQL
    Si retornar_dataframe=True, devuelve el DataFrame limpio.
    """
    print("🚀 Iniciando proceso ETL...")

    # --- 1️⃣ EXTRAER ---
    df_raw = extraer_datos()

    # --- 2️⃣ TRANSFORMAR ---
    df_clean = transformar_datos(df_raw)

    # --- 3️⃣ CARGAR ---
    model = DataModel()
    model.guardar_datos(df_clean)
    model.cerrar_conexion()

    print("✅ ETL completado correctamente.")

    # --- 4️⃣ Retornar dataframe si se solicita ---
    if retornar_dataframe:
        return df_clean
