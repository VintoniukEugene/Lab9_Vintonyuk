import psycopg2
from faker import Faker
import random

# Налаштування підключення (як у docker-compose)
DB_CONFIG = {
    'dbname': 'university_db',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5433'
}

fake = Faker('uk_UA')  # Українська локалізація

def create_tables():
    commands = [
        # Таблиця 1: Студенти
        """
        DROP TABLE IF EXISTS exams;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS subjects;
        
        CREATE TABLE students (
            student_id SERIAL PRIMARY KEY,
            surname VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            patronymic VARCHAR(50),
            address TEXT,
            phone VARCHAR(20),
            course INTEGER CHECK (course >= 1 AND course <= 4),
            faculty VARCHAR(100),
            group_name VARCHAR(20),
            is_head BOOLEAN DEFAULT FALSE
        )
        """,
        # Таблиця 2: Предмети
        """
        CREATE TABLE subjects (
            subject_id SERIAL PRIMARY KEY,
            subject_name VARCHAR(100) NOT NULL,
            hours INTEGER,
            semesters INTEGER
        )
        """,
        # Таблиця 3: Іспити (Зв'язки One-to-Many)
        """
        CREATE TABLE exams (
            exam_id SERIAL PRIMARY KEY,
            exam_date DATE,
            student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
            subject_id INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
            grade INTEGER CHECK (grade >= 2 AND grade <= 5)
        )
        """
    ]
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Таблиці успішно створені.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка: {error}")
    finally:
        if conn is not None:
            conn.close()

def populate_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 1. Генерація 3 предметів
    subjects_data = [
        ("Вища математика", 120, 2),
        ("Програмування Python", 90, 1),
        ("Бази даних", 60, 1)
    ]
    for sub in subjects_data:
        cur.execute("INSERT INTO subjects (subject_name, hours, semesters) VALUES (%s, %s, %s)", sub)

    # 2. Генерація 11 студентів
    faculties = ["ІТ", "Економічний", "Аграрний менеджмент"]
    
    for _ in range(11):
        surname = fake.last_name()
        name = fake.first_name()
        patronymic = fake.first_name_male() + "ович" if random.choice([True, False]) else fake.first_name_female() + "івна"
        address = fake.address()
        phone = f"+380{random.randint(100000000, 999999999)}"
        course = random.randint(1, 4)
        faculty = random.choice(faculties)
        group_name = f"{faculty[0]}-{course}{random.randint(1, 3)}"
        is_head = random.choice([True, False])

        cur.execute("""
            INSERT INTO students (surname, name, patronymic, address, phone, course, faculty, group_name, is_head)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (surname, name, patronymic, address, phone, course, faculty, group_name, is_head))

    # 3. Генерація іспитів (кожен студент склав хоча б 1 іспит)
    cur.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT subject_id FROM subjects")
    subject_ids = [row[0] for row in cur.fetchall()]

    for stud_id in student_ids:
        # Кожен студент здає всі 3 предмети
        for sub_id in subject_ids:
            exam_date = fake.date_between(start_date='-1y', end_date='today')
            grade = random.randint(2, 5)
            cur.execute("""
                INSERT INTO exams (exam_date, student_id, subject_id, grade)
                VALUES (%s, %s, %s, %s)
            """, (exam_date, stud_id, sub_id, grade))

    conn.commit()
    cur.close()
    conn.close()
    print("Дані успішно додані (Faker).")

if __name__ == "__main__":
    create_tables()
    populate_data()