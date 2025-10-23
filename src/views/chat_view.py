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
                "Eres Águila 🦅, un asistente inteligente del SENA. "
                "Hablas en español con empatía y claridad. "
                "Ayudas a comunidades en temas de educación, salud, medio ambiente y seguridad.\n\n"
                "Estos son ejemplos reales:\n" + base_conocimiento
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
