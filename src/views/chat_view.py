# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
import pandas as pd
from collections import deque

app = Flask(__name__, template_folder="templates", static_folder="static")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:1.5b-instruct"

# ====================================================
# 📦 Cargar base de conocimiento desde MySQL
# ====================================================
def cargar_datos_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="comunidad_1"
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
        return f"(⚠️ Error cargando base de datos: {e})"

base_conocimiento = cargar_datos_mysql()

# ====================================================
# 💾 Memoria ligera (solo 3 mensajes)
# ====================================================
memoria = deque(maxlen=3)
contador_turnos = 0

# ====================================================
# 💬 API DE CHAT
# ====================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    global contador_turnos
    data = request.get_json()
    mensaje_usuario = data.get("message", "").strip()

    memoria.append({"role": "user", "content": mensaje_usuario})
    contador_turnos += 1

    # 🧠 Refuerzo del rol cada 3 turnos
    if contador_turnos % 3 == 0:
        system_prompt = (
            "Eres **KELU 🦅**, una inteligencia artificial comunitaria del SENA. "
            "Tu propósito es resolver cualquier problema doméstico o comunitario "
            "con empatía y pasos concretos. "
            "Siempre responde en cuatro partes: empatía, análisis, soluciones (3-5 pasos) y cierre positivo. "
            "Nunca hagas preguntas, ni te desvíes del tema."
        )
    else:
        system_prompt = "Recuerda: eres KELU 🦅, IA de ayuda comunitaria. Da siempre soluciones prácticas y positivas."

    history = [{"role": "system", "content": system_prompt}]
    history.extend(list(memoria))  # solo últimos mensajes

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": history, "stream": False},
            timeout=90
        )
        data = response.json()
        respuesta = data.get("message", {}).get("content", "").strip()

        if not respuesta or len(respuesta) < 20:
            respuesta = "🌱 Intenta lo siguiente: revisa lo básico y busca apoyo comunitario. Todo problema tiene solución."

    except Exception as e:
        respuesta = f"(⚠️ Error al contactar el modelo: {e})"

    memoria.append({"role": "assistant", "content": respuesta})
    return jsonify({"reply": respuesta})

# ====================================================
# 🚀 INICIO DEL SERVIDOR
# ====================================================
@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    print("🚀 KELU IA optimizado con contexto inteligente 🦅")
    print("👉 Abre: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
