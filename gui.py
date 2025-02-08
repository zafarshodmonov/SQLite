import sqlite3
import tkinter as tk
from tkinter import scrolledtext, messagebox
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Database yaratish uchun funksiya
def create_database():
    dbs = {}
    for db_name in ["students", "employees", "products", "orders"]:
        conn = sqlite3.connect(f":memory:")
        cursor = conn.cursor()
        if db_name == "students":
            cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                grade TEXT
            )
            """)
            data = [(fake.name(), random.randint(18, 30), random.choice(["A", "B", "C", "D"])) for _ in range(100)]
            cursor.executemany("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", data)
        elif db_name == "employees":
            cursor.execute("""
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary INTEGER
            )
            """)
            data = [(fake.name(), random.choice(["HR", "IT", "Finance", "Marketing"]), random.randint(30000, 100000)) for _ in range(100)]
            cursor.executemany("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", data)
        elif db_name == "products":
            cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL
            )
            """)
            data = [(fake.word(), random.choice(["Electronics", "Clothing", "Food", "Furniture"]), round(random.uniform(10, 500), 2)) for _ in range(100)]
            cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", data)
        elif db_name == "orders":
            cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                customer TEXT,
                product TEXT,
                amount INTEGER
            )
            """)
            data = [(fake.name(), fake.word(), random.randint(1, 10)) for _ in range(100)]
            cursor.executemany("INSERT INTO orders (customer, product, amount) VALUES (?, ?, ?)", data)
        conn.commit()
        dbs[db_name] = (conn, cursor)
    return dbs

# Masalalarni bazadan yuklash
def load_questions():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, db_name, question, correct_query FROM problems")
    questions = cursor.fetchall()
    conn.close()
    return questions

databases = create_database()
questions = load_questions()
current_question = 0

def get_table_schema(db_name):
    schemas = {
        "students": "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, grade TEXT",
        "employees": "id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER",
        "products": "id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL",
        "orders": "id INTEGER PRIMARY KEY, customer TEXT, product TEXT, amount INTEGER"
    }
    return schemas[db_name]

def load_question():
    global current_question
    _, db_name, question_text, _ = questions[current_question]
    schema_info = get_table_schema(db_name)
    question_label.config(text=f"{current_question + 1}. {question_text}\n(Database: {db_name})\nTable Schema: {schema_info}")
    sql_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

def check_answer():
    global current_question
    _, db_name, _, correct_query = questions[current_question]
    user_query = sql_text.get("1.0", tk.END).strip()
    if not user_query:
        messagebox.showwarning("Warning", "Please enter an SQL query.")
        return
    try:
        conn, cursor = databases[db_name]
        cursor.execute(correct_query)
        correct_result = cursor.fetchall()
        cursor.execute(user_query)
        user_result = cursor.fetchall()
        output_text.delete("1.0", tk.END)
        if user_result == correct_result:
            output_text.insert(tk.END, "Correct!\n")
        else:
            output_text.insert(tk.END, "Incorrect! Try again.\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def next_question():
    global current_question
    if current_question < len(questions) - 1:
        current_question += 1
        load_question()
    else:
        messagebox.showinfo("Finished", "You have completed all the questions!")

# GUI yaratish
root = tk.Tk()
root.title("SQL Practice")

question_label = tk.Label(root, text="", wraplength=400, justify="left")
question_label.pack()

sql_text = scrolledtext.ScrolledText(root, height=5, width=50)
sql_text.pack(pady=5)

submit_btn = tk.Button(root, text="Submit", command=check_answer)
submit_btn.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=10, width=50)
output_text.pack(pady=5)

next_btn = tk.Button(root, text="Next", command=next_question)
next_btn.pack(pady=5)

load_question()
root.mainloop()

for conn, _ in databases.values():
    conn.close()
