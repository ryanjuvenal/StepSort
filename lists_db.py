# lists_db.py
import sqlite3
from datetime import datetime

# Nome do arquivo do banco de dados SQLite
DB_LISTS = "lists.db"


# ---------------------------------------------------------
# Cria as tabelas do banco caso ainda não existam
# ---------------------------------------------------------
def create_tables():
    conn = sqlite3.connect(DB_LISTS)   # Abre conexão com o banco
    cursor = conn.cursor()             # Cria cursor para executar SQL

    # Cria tabela "listas" caso não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- ID gerado automaticamente
            jogador TEXT NOT NULL,                  -- Nome do jogador
            algoritmo TEXT NOT NULL,                -- Tipo do algoritmo
            complexidade TEXT NOT NULL,             -- Complexidade do algoritmo
            numeros TEXT NOT NULL,                  -- Lista de números (string)
            data_registro TEXT NOT NULL             -- Data e hora do registro
        )
    """)

    conn.commit()   # Salva alterações
    conn.close()    # Fecha conexão


# ---------------------------------------------------------
# Salva uma lista no banco de dados
# ---------------------------------------------------------
def salvar_lista(jogador: str, numeros: list, algoritmo: str, complexidade: str ):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()

    # Converte a lista de números para string "1,2,3"
    numeros_text = ",".join(str(x) for x in numeros)

    # Data do registro no formato AAAA-MM-DD HH:MM:SS
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insere o registro no banco
    cursor.execute("""
        INSERT INTO listas (jogador, numeros, algoritmo, complexidade, data_registro)
        VALUES (?, ?, ?, ?, ?)
    """, (jogador, numeros_text, algoritmo, complexidade, data))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Lista os registros do banco (limitando quantos retornar)
# ---------------------------------------------------------
def listar_listas(limit: int = 100):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()

    # Busca os registros mais recentes primeiro
    cursor.execute("""
        SELECT id, jogador, numeros, algoritmo, complexidade, data_registro
        FROM listas
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()  # Pega todos os resultados
    conn.close()
    return rows


# ---------------------------------------------------------
# Apaga todos os registros da tabela (usado com cautela)
# ---------------------------------------------------------
def limpar_listas():
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM listas")  # Remove tudo
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Atualiza o nome do jogador em um registro específico
# ---------------------------------------------------------
def atualizar_nome(id_registro, novo_nome):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE listas SET jogador = ? WHERE id = ?",
        (novo_nome, id_registro)
    )

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Remove um registro específico pelo ID
# ---------------------------------------------------------
def deletar_registro(id_registro):
    conn = sqlite3.connect(DB_LISTS)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM listas WHERE id = ?",
        (id_registro,)
    )

    conn.commit()
    conn.close()
