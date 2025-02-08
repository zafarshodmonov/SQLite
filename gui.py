import sqlite3
import tkinter as tk
from tkinter import scrolledtext, messagebox
from faker import Faker
import random

# Initialize Faker
fake = Faker()

def get_table_schema(db_name):
    schemas = {
        "students": "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, grade TEXT",
        "employees": "id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER",
        "products": "id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL",
        "orders": "id INTEGER PRIMARY KEY, customer TEXT, product TEXT, amount INTEGER"
    }
    return schemas[db_name]

current_question = 0

def create_database():
    dbs = {}
    for db_name in ["students", "employees", "products", "orders"]:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE {db_name} ({get_table_schema(db_name)})")
        
        if db_name == "students":
            data = [(fake.name(), random.randint(18, 30), random.choice(["A", "B", "C", "D"])) for _ in range(100)]
            cursor.executemany("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", data)
        elif db_name == "employees":
            data = [(fake.name(), random.choice(["HR", "IT", "Finance", "Marketing"]), random.randint(30000, 100000)) for _ in range(100)]
            cursor.executemany("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", data)
        elif db_name == "products":
            data = [(fake.word(), random.choice(["Electronics", "Clothing", "Food", "Furniture"]), round(random.uniform(10, 500), 2)) for _ in range(100)]
            cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", data)
        elif db_name == "orders":
            data = [(fake.name(), fake.word(), random.randint(1, 10)) for _ in range(100)]
            cursor.executemany("INSERT INTO orders (customer, product, amount) VALUES (?, ?, ?)", data)
        conn.commit()
        dbs[db_name] = (conn, cursor)
    return dbs

databases = create_database()

def load_questions_from_db():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT table_name, question, query FROM sql_questions")
    questions = cursor.fetchall()
    conn.close()
    return questions

questions_list = load_questions_from_db()

def load_question():
    global current_question
    db_name, question_text, _ = questions_list[current_question]
    schema_info = get_table_schema(db_name)
    question_label.config(text=f"{current_question + 1}. {question_text}\n(Database: {db_name})\nTable Schema:\n{schema_info}")
    sql_text.delete("1.0", tk.END)

def check_answer():
    global current_question
    db_name, _, correct_query = questions_list[current_question]
    user_query = sql_text.get("1.0", tk.END).strip()
    if not user_query:
        messagebox.showwarning("Warning", "Please enter an SQL query.")
        return
    try:
        conn, cursor = databases[db_name]
        cursor.execute(user_query)
        user_result = cursor.fetchall()
        cursor.execute(correct_query)
        correct_result = cursor.fetchall()
        
        result_message = "✅ Correct!" if user_result == correct_result else "❌ Incorrect! Try again."
        messagebox.showinfo("Result", result_message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def next_question():
    global current_question
    if current_question < len(questions_list) - 1:
        current_question += 1
        load_question()
    else:
        messagebox.showinfo("Finished", "You have completed all the questions!")

def prev_question():
    global current_question
    if current_question > 0:
        current_question -= 1
        load_question()
    else:
        messagebox.showwarning("Warning", "This is the first question!")

root = tk.Tk()
root.title("SQL Practice")
root.configure(bg="#f0f0f0")

question_label = tk.Label(root, text="", wraplength=500, justify="left", font=("Arial", 12, "bold"), bg="#f0f0f0")
question_label.pack(pady=10)

sql_text = scrolledtext.ScrolledText(root, height=5, width=60, font=("Arial", 10))
sql_text.pack(pady=5)

submit_btn = tk.Button(root, text="Submit", command=check_answer, font=("Arial", 12, "bold"), bg="lightblue")
submit_btn.pack(pady=5)

nav_frame = tk.Frame(root)
nav_frame.pack(pady=5)

back_btn = tk.Button(nav_frame, text="Back", command=prev_question, font=("Arial", 12, "bold"), bg="lightcoral")
back_btn.pack(side=tk.LEFT, padx=5)

next_btn = tk.Button(nav_frame, text="Next", command=next_question, font=("Arial", 12, "bold"), bg="lightgreen")
next_btn.pack(side=tk.LEFT, padx=5)

load_question()
root.mainloop()

for conn, _ in databases.values():
    conn.close()
