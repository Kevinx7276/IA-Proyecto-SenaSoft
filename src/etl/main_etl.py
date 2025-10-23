# -*- coding: utf-8 -*-
from extract import extraer_datos
from transform import transformar_datos
from load import cargar_datos

def main():
    print("🚀 Iniciando proceso ETL del proyecto SENA...")
    datos_crudos = extraer_datos()
    datos_limpios = transformar_datos(datos_crudos)
    cargar_datos(datos_limpios)
    print("✅ ETL completado correctamente.")

if __name__ == "__main__":
    main()
