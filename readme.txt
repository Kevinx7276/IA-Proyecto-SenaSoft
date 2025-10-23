# 🦅 Proyecto KELU IA – Asistente Comunitario del SENA

> **Desarrollado para el Reto Nacional SENA-Soft 2025**  
> Solución basada en Inteligencia Artificial que analiza, clasifica y propone soluciones a problemas comunitarios en Colombia usando datos reales del entorno social.

---

## 📘 Descripción del Proyecto

**KELU IA** es un asistente virtual inteligente, empático y ético diseñado para ayudar a los ciudadanos a resolver problemas comunitarios en las áreas de:

- 🌱 **Medio Ambiente** – recolección de basuras, contaminación, reciclaje.  
- 🏥 **Salud** – acceso a hospitales, atención médica, prevención.  
- 🎓 **Educación** – infraestructura escolar, acceso a bibliotecas, formación.  
- 🚨 **Seguridad** – robos, vigilancia, alumbrado público.  
- 🏗️ **Infraestructura** – calles, carreteras, obras públicas.  

La solución utiliza **técnicas de procesamiento de lenguaje natural (NLP)**, **aprendizaje automático local** y **búsqueda semántica**, integrando:

- **ETL (Extract, Transform, Load)** para procesar y limpiar datos de comunidades.
- **FAISS** y **Sentence Transformers** para búsqueda de similitud semántica.
- **Modelo de lenguaje local (Ollama + Qwen2)** para generación natural de respuestas.
- **Arquitectura MVC (Modelo–Vista–Controlador)** para mantener escalabilidad y organización.

---

## 🧩 Arquitectura del Proyecto

IA-Proyecto-SenaSoft/
│
├── data/ # Datos, resultados y registros
│ ├── dataset_comunidades_senasoft.csv
│ ├── resultados_parciales.csv
│ ├── embeddings_meta.parquet
│ ├── index.faiss
│ └── historial_conversaciones.csv
│
├── src/
│ ├── etl/ # Proceso ETL
│ │ ├── extract.py
│ │ ├── transform.py
│ │ ├── load.py
│ │ └── main_etl.py
│ │
│ ├── models/ # Capa Modelo (acceso a datos y base de conocimiento)
│ │ 
│ │ └── data_model.py
│ │
│ ├── controllers/ # Capa Controlador
│ │ └── etl_controller.py
│ │
│ ├── views/ # Capa Vista (interfaces, si aplica)
│ │ └── ...
│ │
│ └── app.py # Punto de entrada principal del sistema
      conexion_mysql.py
      ethics.py
      evaluate_model.py
      visualize_results.py
│
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo


---

## ⚙️ Instalación y Configuración

### 🧠 Requisitos previos

- **Python 3.10+**
- **MySQL Server** con una base de datos creada (ej. `senasoft`)
- **Ollama** (para ejecutar modelos IA localmente sin conexión)

Instala Ollama desde:  
👉 [https://ollama.com/download](https://ollama.com/download)

Y descarga el modelo base gratuito:
```bash
ollama pull qwen2:1.5b-instruct
