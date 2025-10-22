import pandas as pd
from transformers import pipeline
from conexion_mysql import conectar_a_mysql  # Importamos la función de conexión

# Cargar el pipeline de clasificación de texto de Hugging Face
classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased")

# Definir las categorías posibles
categorias_posibles = ["Medio Ambiente", "Educación", "Seguridad", "Salud", "Infraestructura", "Otro"]

# Conectar a la base de datos MySQL
mydb = conectar_a_mysql()
if mydb is None:
    print("No se pudo conectar a la base de datos. Terminando el proceso.")
    exit()

mycursor = mydb.cursor()

# Cargar el archivo CSV con los datos
file_path = '../data/dataset_comunidades_senasoft.csv'
df = pd.read_csv(file_path)

# Eliminar filas con valores NaN en la columna 'Comentario' (si hay comentarios vacíos o nulos)
df = df.dropna(subset=['Comentario'])

# Detectar columna de "urgencia"
col_urgencia = next((c for c in df.columns if any(k in c.lower() for k in ['urgenc', 'urgente', 'prioridad'])), None)
print(f"Columna para urgencia detectada: {col_urgencia}")

# Función para analizar un solo comentario usando Hugging Face Zero-Shot Classification
def analizar_comentario_huggingface(comentario):
    try:
        # Realizar clasificación en las categorías predefinidas
        result = classifier(comentario, candidate_labels=categorias_posibles)
        categorias = result['labels']  # Extraer las etiquetas de categoría
        return categorias
    except Exception as e:
        print(f"Error analizando el comentario: {comentario}. Error: {str(e)}")
        return []

# Función para insertar los resultados en MySQL (inserción en lote de 10 comentarios)
def insertar_en_mysql_lote(comentarios, categorias, ciudades, urgencias):
    try:
        # Convertir las listas de categorías en cadenas de texto (por ejemplo, 'Seguridad, Medio Ambiente')
        categorias_str = [', '.join(categorias[i]) for i in range(len(categorias))]
        
        # Crear una lista de valores para insertar en MySQL
        insert_values = [(comentarios[i], ciudades[i], urgencias[i], categorias_str[i]) for i in range(len(comentarios))]
        
        # Insertar todos los comentarios en una sola operación
        sql_comentario = """
        INSERT INTO comentarios (Comentario, Ciudad, NivelDeUrgencia, Categorias) 
        VALUES (%s, %s, %s, %s)
        """
        mycursor.executemany(sql_comentario, insert_values)
        mydb.commit()
        print(f"Comentarios insertados: {len(comentarios)}")
    except Exception as e:
        print(f"Error insertando en MySQL: {str(e)}")

# Función para procesar cada lote de 10 comentarios
def procesar_lote(lote):
    comentarios = []
    categorias = []
    ciudades = []
    urgencias = []

    # Procesar cada comentario en el lote
    for index, row in lote.iterrows():
        categorias_comentario = analizar_comentario_huggingface(row['Comentario'])
        comentarios.append(row['Comentario'])
        categorias.append(categorias_comentario)
        ciudades.append(row['Ciudad'])  # Obtener la ubicación de la columna 'Ciudad'
        urgencias.append(row['Nivel de urgencia'])  # Obtener el nivel de urgencia de la columna 'Nivel de urgencia'

        # Asignar las categorías al DataFrame (en la columna correcta)
        lote.at[index, 'Categoría del problema'] = ', '.join(categorias_comentario)  # Convertir en cadena

    # Insertar los comentarios procesados en lote
    insertar_en_mysql_lote(comentarios, categorias, ciudades, urgencias)

    # Guardar el progreso en un archivo CSV
    df_subset_filtered = lote[['Comentario', 'Ciudad', 'Nivel de urgencia', 'Categoría del problema']]
    df_subset_filtered.to_csv('../data/resultados_parciales.csv', index=False, encoding='utf-8')
    print(f"💾 Progreso guardado para comentarios {lote.index[0] + 1} a {lote.index[-1] + 1}")

# Función para procesar el dataset en lotes pequeños y almacenar en MySQL
def procesar_lotes(df, batch_size=10):  # Procesar en lotes de 10 para manejar los 10k
    total_comments = len(df)
    num_batches = (total_comments // batch_size) + (1 if total_comments % batch_size > 0 else 0)
    
    print(f"Total de comentarios: {total_comments}")
    print(f"Total de lotes: {num_batches}")

    # Procesar en lotes de 10 de forma secuencial (sin paralelización)
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, total_comments)
        print(f"\nProcesando comentarios {start_idx + 1} a {end_idx}...")

        batch = df.iloc[start_idx:end_idx]  # Obtener el lote actual

        # Procesar el lote actual
        procesar_lote(batch)

# Iniciar el procesamiento del dataset
procesar_lotes(df, batch_size=10)  # Aquí procesamos en lotes de 10 para los 10,000 comentarios

# Cerrar la conexión a la base de datos
mycursor.close()
mydb.close()