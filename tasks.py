import sqlite3

def create_tasks_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Tasks jadvalini yaratamiz
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        db_name TEXT,
        question TEXT,
        correct_query TEXT
    )
    """)

    # Masalalar ro‘yxati
    questions = [
        ("students", "Find all students older than 25", "SELECT * FROM students WHERE age > 25"),
        ("students", "Count the number of students with grade A", "SELECT COUNT(*) FROM students WHERE grade = 'A'"),
        ("employees", "List all employees in IT department", "SELECT * FROM employees WHERE department = 'IT'"),
        ("employees", "Find the highest salary in the employees table", "SELECT MAX(salary) FROM employees"),
        ("products", "List all products that cost more than 100", "SELECT * FROM products WHERE price > 100"),
        ("products", "Find the average price of all products", "SELECT AVG(price) FROM products"),
        ("orders", "Count the total number of orders", "SELECT COUNT(*) FROM orders"),
        ("orders", "Find all orders where amount is more than 5", "SELECT * FROM orders WHERE amount > 5")
    ] * 6  # 50 ta masala hosil qilish uchun ko‘paytiramiz

    # Masalalarni DB ga yozamiz
    cursor.executemany("INSERT INTO problems (db_name, question, correct_query) VALUES (?, ?, ?)", questions)
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, db_name, question, correct_query FROM problems")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

if __name__ == "__main__":
    create_tasks_database()
    print("Tasks database created and populated.")
