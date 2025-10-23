import os
import sys

# Añadir la carpeta padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexion_mysql import conectar_a_mysql

# -*- coding: utf-8 -*-
from conexion_mysql import conectar_a_mysql

def cargar_datos(df):
    print("💾 Cargando datos limpios en MySQL...")

    mydb = conectar_a_mysql()
    if mydb is None:
        print("❌ Error: no se pudo conectar a la base de datos.")
        return

    mycursor = mydb.cursor()

    # Crear tabla si no existe
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS comentarios_limpios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Comentario TEXT,
        Ciudad VARCHAR(100),
        NivelDeUrgencia VARCHAR(50),
        LongitudComentario INT
    )
    """)

    # Insertar los datos
    for _, row in df.iterrows():
        sql = """
        INSERT INTO comentarios_limpios (Comentario, Ciudad, NivelDeUrgencia, LongitudComentario)
        VALUES (%s, %s, %s, %s)
        """
        values = (row["Comentario"], row["Ciudad"], row["Nivel De Urgencia"], row["LongitudComentario"])
        mycursor.execute(sql, values)

    mydb.commit()
    mydb.close()
    print("✅ Carga completa en MySQL.")
