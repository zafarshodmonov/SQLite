import sqlite3
import json

# JSON faylni ochamiz
with open('questions.json', 'r') as f:
    questions = json.load(f)

# SQLite bazasiga ulanamiz
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Jadvalni yaratamiz
cursor.execute("""
CREATE TABLE IF NOT EXISTS sql_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    question TEXT,
    query TEXT
)
""")

# Ma'lumotlarni qo'shamiz
for q in questions:
    cursor.execute("INSERT INTO sql_questions (table_name, question, query) VALUES (?, ?, ?)", 
                   (q["table"], q["question"], q["query"]))

conn.commit()
conn.close()
