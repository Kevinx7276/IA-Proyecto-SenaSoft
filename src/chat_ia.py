# -*- coding: utf-8 -*-
"""
KELU IA Comunitaria – Modo Libre Total
Autor: SENA / SENASoft 2025

Este módulo permite que la IA converse libremente con razonamiento completo,
usando los datos de la base como inspiración, pero con autonomía total para responder.
"""

import os
import pandas as pd
import mysql.connector
import requests

# ===================================================
# ⚙️ CONFIGURACIÓN GENERAL
# ===================================================
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b-instruct"  # Puedes cambiarlo por mistral:instruct, qwen2:1.5b-instruct, etc.


# ===================================================
# 📦 FUNCIÓN: CARGAR EJEMPLOS DESDE MYSQL
# ===================================================
def cargar_datos_mysql():
    """
    Recupera ejemplos desde la base de datos MySQL para que el modelo los use como inspiración.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",  # Cambia si es diferente
            database="senasoft"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Comentario, Ciudad, NivelDeUrgencia, Categorias FROM comentarios LIMIT 150;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not data:
            return "No hay ejemplos en la base de datos todavía."

        df = pd.DataFrame(data)
        ejemplos = []
        for _, row in df.iterrows():
            ejemplos.append(
                f"- ({row.get('Categorias', 'Sin categoría')}) {row.get('Comentario', '').strip()} "
                f"[Urgencia: {row.get('NivelDeUrgencia', 'N/A')}, Ciudad: {row.get('Ciudad', 'Desconocida')}]"
            )
        return "\n".join(ejemplos)

    except Exception as e:
        return f"(Error al cargar datos: {e})"


# ===================================================
# 💬 FUNCIÓN PRINCIPAL: CHAT IA
# ===================================================
def iniciar_chat_ia():
    """
    Inicia el chat interactivo con la IA KELU.
    Usa ejemplos de la base de datos solo como conocimiento base,
    pero permite respuestas autónomas y naturales.
    """
    print("📡 Cargando base de conocimiento desde MySQL...")
    contexto_base = cargar_datos_mysql()

    print(f"🤖 KELU IA (modelo: {MODEL}) lista para conversar.")
    print("Escribe 'salir' para terminar.\n")

    # 🧠 Identidad y reglas base de la IA
    history = [
        {
            "role": "system",
            "content": (
                "Eres KELU 🦅, una inteligencia artificial comunitaria desarrollada por el SENA. "
                "Fuiste entrenada para comprender y conversar con personas sobre cualquier tema, "
                "con empatía, claridad y pensamiento crítico. Puedes hablar libremente sobre salud, "
                "educación, medio ambiente, seguridad y otros temas de la vida cotidiana. "
                "No estás restringida: tu misión es ayudar, analizar y orientar de forma respetuosa y útil.\n\n"

                "Usa el conocimiento proveniente de los datos ciudadanos solo como contexto de referencia:\n"
                f"{contexto_base}\n\n"

                "Tus respuestas deben ser completas, útiles y bien redactadas. "
                "No repitas texto literal del contexto, razona por ti misma. "
                "Si un usuario te pide consejos, sugerencias o explicaciones, ofrécelas con lógica y empatía. "
                "Puedes usar ejemplos, listas o pasos prácticos si es necesario. "
                "No digas que no puedes ayudar: siempre busca orientar, informar o guiar con criterio humano."
            )
        }
    ]

    # 🔁 Bucle conversacional
    while True:
        user = input("👤 Tú: ").strip()
        if user.lower() in {"salir", "exit", "quit"}:
            print("👋 ¡Hasta luego! Cuídate mucho.")
            break

        history.append({"role": "user", "content": user})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": history, "stream": False},
                timeout=120
            )
            data = response.json()
            ai = data.get("message", {}).get("content", "").strip()
        except Exception as e:
            ai = f"(Error al contactar modelo: {e})"

        print(f"\n🦅 KELU: {ai}\n")
        history.append({"role": "assistant", "content": ai})


# ===================================================
# 🚀 EJECUCIÓN DIRECTA
# ===================================================
if __name__ == "__main__":
    iniciar_chat_ia()
