# conexion_mysql.py
import mysql.connector

def conectar_a_mysql():
    try:
        # Configuración de la conexión a MySQL
        mydb = mysql.connector.connect(
            host="localhost",        # Dirección del servidor MySQL
            user="root",             # Usuario de MySQL
            password="", # Contraseña de MySQL
            database="comunidad_1"     # Nombre de la base de datos
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error de conexión a MySQL: {err}")
        return None
