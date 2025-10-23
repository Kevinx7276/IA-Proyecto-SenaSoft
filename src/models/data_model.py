# -*- coding: utf-8 -*-
"""
DataModel – Gestión de conexión y operaciones con MySQL
Parte del sistema Águila IA Comunitaria (MVC)
"""

import pandas as pd
from conexion_mysql import conectar_a_mysql

class DataModel:
    """Clase que gestiona operaciones de base de datos para el ETL y la IA."""

    def __init__(self):
        self.conn = conectar_a_mysql()
        if self.conn:
            print("✅ Conexión establecida desde DataModel.")
        else:
            print("❌ No se pudo establecer conexión MySQL desde DataModel.")

    # -----------------------------------------------------------
    # Guardar datos limpios en MySQL
    # -----------------------------------------------------------
    def guardar_datos(self, df: pd.DataFrame):
        """Inserta el DataFrame procesado en la tabla comentarios_limpios."""
        if self.conn is None or df is None or df.empty:
            print("⚠️ No hay conexión o DataFrame vacío.")
            return

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios_limpios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Comentario TEXT,
            Ciudad VARCHAR(100),
            NivelDeUrgencia VARCHAR(50),
            Categorias VARCHAR(100),
            Razon TEXT,
            LongitudComentario INT
        )
        """)

        for _, row in df.iterrows():
            sql = """
            INSERT INTO comentarios_limpios 
            (Comentario, Ciudad, NivelDeUrgencia, Categorias, Razon, LongitudComentario)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                row.get("Comentario", ""),
                row.get("Ciudad", ""),
                row.get("NivelDeUrgencia", ""),
                row.get("Categorias", ""),
                row.get("Razon", ""),
                int(row.get("LongitudComentario", 0))
            )
            cursor.execute(sql, values)

        self.conn.commit()
        print(f"💾 {len(df)} registros insertados correctamente en MySQL.")

    # -----------------------------------------------------------
    # Leer datos desde la tabla
    # -----------------------------------------------------------
    def leer_datos(self, limite=50):
        """Devuelve un DataFrame con los datos almacenados."""
        if self.conn is None:
            print("⚠️ No hay conexión a MySQL.")
            return pd.DataFrame()

        query = f"SELECT * FROM comentarios_limpios LIMIT {limite};"
        df = pd.read_sql(query, self.conn)
        return df

    # -----------------------------------------------------------
    # Cerrar conexión
    # -----------------------------------------------------------
    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            print("🔒 Conexión MySQL cerrada.")
