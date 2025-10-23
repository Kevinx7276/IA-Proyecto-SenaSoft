# -*- coding: utf-8 -*-
"""
Módulo de conversación Águila IA Comunitaria
Vista: Interacción con el usuario (CLI)
Autor: SENA / SENASoft 2025
"""

import os
import pandas as pd
import mysql.connector
import requests

# ===================================================
# CONFIGURACIÓN GENERAL
# ===================================================
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2:1.5b-instruct"

# ===================================================
# FUNCIÓN: CARGAR DATOS DESDE MYSQL
# ===================================================
def cargar_datos_mysql():
    """
    Recupera ejemplos desde la base de datos MySQL
    para contextualizar al modelo.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",  # cambia si es diferente
            database="senasoft"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Comentario, Ciudad, NivelDeUrgencia, Categorias FROM comentarios LIMIT 200;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not data:
            return "No hay datos en la base de datos."

        df = pd.DataFrame(data)
        ejemplos = []
        for _, row in df.iterrows():
            ejemplos.append(
                f"- ({row.get('Categorias', 'Sin categoría')}) {row.get('Comentario', '').strip()} "
                f"[Urgencia: {row.get('NivelDeUrgencia', 'N/A')}, Ciudad: {row.get('Ciudad', 'Desconocida')}]"
            )
        contexto = "\n".join(ejemplos)
        return contexto

    except Exception as e:
        return f"(Error cargando base de datos: {e})"


# ===================================================
# FUNCIÓN PRINCIPAL DE CHAT
# ===================================================
def iniciar_chat_ia():
    """
    Inicia el chat interactivo con el modelo Qwen2.
    Usa ejemplos desde la base de datos como conocimiento contextual.
    """
    print("📦 Cargando información desde MySQL...")
    base_conocimiento = cargar_datos_mysql()

    print(f"🤖 Águila (modelo: {MODEL}) lista para conversar.")
    print("Escribe 'salir' para terminar.\n")

    history = [
        {
            "role": "system",
            "content": (
                "Eres Kelu, un asistente amable e inteligente del SENA. "
                "Hablas siempre en español, con frases naturales, claras y cortas. "
                "Tu función es ayudar a las comunidades a resolver problemas reales "
                "en temas de educación, salud, medio ambiente y seguridad.\n\n"
                "Estos son ejemplos de situaciones reales que conoces:\n"
                f"{base_conocimiento}\n\n"
                "Usa este conocimiento solo como referencia para entender los problemas más comunes "
                "y dar soluciones útiles, sin mencionar nombres ni lugares específicos."
            )
        }
    ]

    # Bucle conversacional
    while True:
        user = input("👤 Tú: ").strip()
        if user.lower() in {"salir", "exit", "quit"}:
            print("👋 ¡Hasta luego! Cuídate.")
            break

        history.append({"role": "user", "content": user})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": history, "stream": False},
                timeout=90
            )
            data = response.json()
            ai = data.get("message", {}).get("content", "").strip()
        except Exception as e:
            ai = f"(Error al contactar modelo: {e})"

        print(f"\n🦅 Águila: {ai}\n")
        history.append({"role": "assistant", "content": ai})
