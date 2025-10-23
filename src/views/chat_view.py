# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="static")

# Configuración del modelo local
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:1.5b-instruct"

# ====================================================
# 🧩 Cargar base de conocimiento desde MySQL
# ====================================================
def cargar_datos_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="senasoft"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Comentario, Ciudad, NivelDeUrgencia, Categorias FROM comentarios LIMIT 100;")
        data = cursor.fetchall()
        conn.close()

        if not data:
            return ""
        df = pd.DataFrame(data)
        ejemplos = [
            f"- ({row['Categorias']}) {row['Comentario']} [Urgencia: {row['NivelDeUrgencia']}, Ciudad: {row['Ciudad']}]"
            for _, row in df.iterrows()
        ]
        return "\n".join(ejemplos)
    except Exception as e:
        return f"(Error cargando base de datos: {e})"

base_conocimiento = cargar_datos_mysql()

# ====================================================
# 🧠 RUTA PRINCIPAL
# ====================================================
@app.route("/")
def index():
    return render_template("chat.html")

# ====================================================
# 💬 ENDPOINT DE CHAT
# ====================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get("message", "")

    history = [
        {
    "role": "system",
    "content": (
        "Eres KELU 🦅, una inteligencia artificial comunitaria creada por el SENA. "
        "Tu misión es analizar y comprender información proveniente de los reportes ciudadanos "
        "guardados en la base de datos. Cada registro contiene un comentario, la ciudad, el nivel de urgencia "
        "y una categoría temática (Educación, Salud, Medio Ambiente o Seguridad). "
        "Usa ese conocimiento para aprender sobre las necesidades de las comunidades y ofrecer respuestas útiles. "
        "Puedes hablar de cualquier tema, incluyendo hospitales, colegios, medio ambiente, o seguridad pública, "
        "siempre de forma respetuosa, informativa y sin hacer diagnósticos médicos ni promesas de acción. "
        "Tu objetivo es orientar, informar y empatizar, usando ejemplos de los datos que ya conoces. "
        "Cuando no tengas información específica, responde con sentido común y ofrece orientación general."
        )
    },
        {"role": "user", "content": mensaje_usuario}
    ]

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": history, "stream": False},
            timeout=60
        )
        respuesta = response.json().get("message", {}).get("content", "")
    except Exception as e:
        respuesta = f"(Error al contactar el modelo: {e})"

    return jsonify({"reply": respuesta})

# ====================================================
# 🚀 Iniciar servidor
# ====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
