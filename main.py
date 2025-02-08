import sqlite3
from faker import Faker

# Bog‘lanish
conn = sqlite3.connect("large_database.db")
cursor = conn.cursor()

# Jadval yaratish
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
)
''')

# Faker orqali 1 million foydalanuvchi qo‘shish
fake = Faker()
data = [(fake.name(), fake.email(), fake.random_int(18, 80)) for _ in range(1_000_000)]

cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", data)
conn.commit()
conn.close()
