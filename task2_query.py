import psycopg2
import pandas as pd

DB_CONFIG = {
    'dbname': 'university_db',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5433'
}

def run_query(title, sql, params=None):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        # Використовуємо pandas для читання SQL і красивого виводу
        df = pd.read_sql_query(sql, conn, params=params)
        print(f"\n=== {title} ===")
        if df.empty:
            print("Результатів немає.")
        else:
            # Налаштування pandas для відображення всіх стовпців
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Помилка у запиті '{title}': {e}")
    finally:
        conn.close()

# --- ЗАПИТИ ВАРІАНТУ 1 ---

# 1. Відобразити всіх студентів, які є старостами, відсортувати прізвища за алфавітом
sql1 = """
SELECT surname, name, group_name, is_head 
FROM students 
WHERE is_head = TRUE 
ORDER BY surname;
"""

# 2. Порахувати середній бал для кожного студента (підсумковий запит)
sql2 = """
SELECT s.surname, s.name, ROUND(AVG(e.grade), 2) as average_grade
FROM students s
JOIN exams e ON s.student_id = e.student_id
GROUP BY s.student_id, s.surname, s.name;
"""

# 3. Для кожного предмета порахувати загальну кількість годин (обчислювальне поле)
# Логіка: Години за семестр * Кількість семестрів
sql3 = """
SELECT subject_name, hours, semesters, (hours * semesters) as total_study_hours
FROM subjects;
"""

# 4. Відобразити успішність студентів по обраному предмету (запит з параметром)
selected_subject = "Програмування Python"
sql4 = """
SELECT s.surname, sub.subject_name, e.grade
FROM exams e
JOIN students s ON e.student_id = s.student_id
JOIN subjects sub ON e.subject_id = sub.subject_id
WHERE sub.subject_name = %s;
"""

# 5. Порахувати кількість студентів на кожному факультеті (підсумковий запит)
sql5 = """
SELECT faculty, COUNT(student_id) as student_count
FROM students
GROUP BY faculty;
"""

# 6. Перехресний запит: Оцінки кожного студента по кожному предмету
# Використовуємо CASE WHEN для імітації Pivot таблиці (найбільш універсальний метод в SQL)
sql6 = """
SELECT 
    s.surname,
    MAX(CASE WHEN sub.subject_name = 'Вища математика' THEN e.grade END) AS Math,
    MAX(CASE WHEN sub.subject_name = 'Програмування Python' THEN e.grade END) AS Python,
    MAX(CASE WHEN sub.subject_name = 'Бази даних' THEN e.grade END) AS DB
FROM students s
JOIN exams e ON s.student_id = e.student_id
JOIN subjects sub ON e.subject_id = sub.subject_id
GROUP BY s.student_id, s.surname;
"""

if __name__ == "__main__":
    run_query("1. Старости (за алфавітом)", sql1)
    run_query("2. Середній бал студентів", sql2)
    run_query("3. Загальна кількість годин предметів", sql3)
    run_query(f"4. Успішність по предмету: {selected_subject}", sql4, (selected_subject,))
    run_query("5. Кількість студентів на факультетах", sql5)
    run_query("6. Зведена таблиця оцінок", sql6)