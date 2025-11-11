# lists_db.py
import sqlite3
from datetime import datetime

DB_LISTS = "lists.db"

def create_tables():
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador TEXT NOT NULL,
            numeros TEXT NOT NULL,
            data_registro TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def salvar_lista(jogador: str, numeros: list):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()
    numeros_text = ",".join(str(x) for x in numeros)
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO listas (jogador, numeros, data_registro)
        VALUES (?, ?, ?)
    """, (jogador, numeros_text, data))
    conn.commit()
    conn.close()

def listar_listas(limit: int = 100):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, jogador, numeros, data_registro
        FROM listas
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
