import pandas as pd
import time
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from conexion_mysql import conectar_a_mysql  # Importamos la función de conexión

# Configuración con la API Key y la URL de IBM Watson
api_key = 'Fb8avwDjaJZ-2RXVD5zmy3rUHcP1OLAiJ1WRr0BD9R1C'  # Tu API Key
url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/2dbfe07f-df30-4a46-a90e-7732b06347b3'  # Tu URL del servicio

# Diccionario de traducción de categorías de inglés a español
categoria_traduccion = {
    "/society/crime": "Crimen",
    "/art and entertainment": "Arte y Entretenimiento",
    "/business and industry": "Negocios e Industria",
    "/science/ecology": "Ciencia y Ecología",
    "/education/special education": "Educación Especial",
    "/health and fitness": "Salud y Acondicionamiento Físico",
    "/family and parenting": "Familia y Crianza",
    # Agrega aquí todas las categorías que necesites traducir
}

# Autenticación en IBM Watson NLU
authenticator = IAMAuthenticator(api_key)
nlu = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
nlu.set_service_url(url)

# Conectar a la base de datos MySQL
mydb = conectar_a_mysql()
if mydb is None:
    print("No se pudo conectar a la base de datos. Terminando el proceso.")
    exit()

mycursor = mydb.cursor()

# Cargar el archivo CSV con los datos
file_path = 'C:/Users/SENA Risaralda/Desktop/Proyecto-IA/IA-Proyecto-SenaSoft/dataset_comunidades_senasoft.csv'
df = pd.read_csv(file_path)

# Eliminar filas con valores NaN en la columna 'Comentario' (si hay comentarios vacíos o nulos)
df = df.dropna(subset=['Comentario'])

# Función para analizar el comentario usando Watson NLU
def analizar_comentario(comentario, umbral=0.7):
    try:
        # Convertir los comentarios que no son cadenas vacías o NaN en None
        if not isinstance(comentario, str) or comentario.strip() == "":
            return [], []  # Si no es un texto válido, devolvemos listas vacías
        
        # Realizar el análisis de categorías con Watson NLU
        response = nlu.analyze(
            text=comentario,
            features={'categories': {}}  # Extraer categorías del texto
        ).get_result()
        
        # Extraer las categorías y sus puntajes
        categorias = [item['label'] for item in response['categories']]
        puntajes = [item['score'] for item in response['categories']]
        
        # Filtrar las categorías por puntaje, manteniendo solo las relevantes (por encima del umbral)
        categorias_relevantes = [
            (categoria, puntaje) for categoria, puntaje in zip(categorias, puntajes) if puntaje >= umbral
        ]
        
        # Traducir todas las categorías relevantes a español
        categorias_traducidas = []
        for categoria, score in categorias_relevantes:
            # Si la categoría existe en el diccionario, traducirla
            if categoria in categoria_traduccion:
                categoria_traducida = categoria_traduccion[categoria]
            else:
                categoria_traducida = categoria  # Si no está en el diccionario, mantenerla en inglés
            categorias_traducidas.append(categoria_traducida)
        
        # Devolver las categorías relevantes en español y sus puntajes
        categorias_filtradas = [cat for cat, score in categorias_relevantes]
        puntajes_filtrados = [score for cat, score in categorias_relevantes]
        
        return categorias_traducidas, puntajes_filtrados
    except Exception as e:
        print(f"Error analizando el comentario: {comentario}. Error: {str(e)}")
        return [], []

# Función para insertar los resultados en MySQL
def insertar_en_mysql(comentario, categorias, puntajes, ciudad, urgencia):
    try:
        # Asegurarse de que 'Ciudad' no sea nulo o vacío
        if not ciudad or ciudad.strip() == "":
            ciudad = "No especificado"  # Asignar un valor por defecto
        
        # Insertar el comentario en la tabla de comentarios
        sql_comentario = "INSERT INTO comentarios (comentario, Ciudad, NivelDeUrgencia, Categorias, Puntajes) VALUES (%s, %s, %s, %s, %s)"
        val_comentario = (comentario, ciudad, urgencia, str(categorias), str(puntajes))
        mycursor.execute(sql_comentario, val_comentario)
        mydb.commit()
          
        mydb.commit()
        print(f"Comentario insertado: {comentario}")
    except Exception as e:
        print(f"Error insertando en MySQL: {str(e)}")


# Función para procesar el dataset en lotes pequeños y almacenar en MySQL
def procesar_lotes(df, batch_size=100):
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]  # Obtener el lote actual
        for index, row in batch.iterrows():
            categorias, puntajes = analizar_comentario(row['Comentario'])
            ciudad = row['Ciudad']  # Obtener la ubicación de la columna 'Ciudad'
            urgencia = row['Nivel de urgencia']  # Obtener el nivel de urgencia de la columna 'Nivel de urgencia'
            if categorias:  # Solo insertamos si hay categorías relevantes
                insertar_en_mysql(row['Comentario'], categorias, puntajes, ciudad, urgencia)  # Insertar en MySQL
        time.sleep(4)  # Esperar 4 segundos entre los lotes para evitar errores de límite de solicitudes

# Procesar el dataset en lotes de 100 filas
procesar_lotes(df, batch_size=100)

# Cerrar la conexión a la base de datos
mycursor.close()
mydb.close()
