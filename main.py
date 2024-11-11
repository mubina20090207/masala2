import sqlite3
from datetime import datetime

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS school (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT(15),
    davlat_maktabi BOOLEAN
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT(15),
    school_id INTEGER,
    FOREIGN KEY(school_id) REFERENCES school(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE,
    gender TEXT NOT NULL,
    school_id INTEGER,
    FOREIGN KEY(school_id) REFERENCES school(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS class (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    school_id INTEGER,
    FOREIGN KEY(teacher_id) REFERENCES teacher(id),
    FOREIGN KEY(school_id) REFERENCES school(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subject (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    class_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY(class_id) REFERENCES class(id),
    FOREIGN KEY(teacher_id) REFERENCES teacher(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS enrollment (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    class_id INTEGER,
    enrollment_date DATE,
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(class_id) REFERENCES class(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grade (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject_id INTEGER,
    grade_value INTEGER,
    date_given DATE,
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(subject_id) REFERENCES subject(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    class_id INTEGER,
    date DATE,
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(class_id) REFERENCES class(id)
);
''')

cursor.execute('ALTER TABLE school RENAME TO school_info')
cursor.execute('ALTER TABLE teacher RENAME TO teacher_info')

cursor.execute('ALTER TABLE student RENAME COLUMN date_of_birth TO dob')
cursor.execute('ALTER TABLE grade RENAME COLUMN date_given TO date_assigned')
cursor.execute('ALTER TABLE subject RENAME COLUMN teacher_id TO instructor_id')

cursor.execute('ALTER TABLE school_info ADD COLUMN email TEXT')
cursor.execute('ALTER TABLE student ADD COLUMN nationality TEXT')

cursor.execute('PRAGMA foreign_keys=off;')
cursor.execute('ALTER TABLE teacher_info RENAME TO teacher_backup')
cursor.execute('CREATE TABLE teacher_info (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, phone_number TEXT(15), school_id INTEGER);')
cursor.execute('INSERT INTO teacher_info SELECT id, first_name, last_name, email, phone_number, school_id FROM teacher_backup;')
cursor.execute('DROP TABLE teacher_backup;')
cursor.execute('PRAGMA foreign_keys=on;')

cursor.execute("UPDATE student SET first_name = 'Akbar' WHERE id = 1")
cursor.execute("UPDATE grade SET grade_value = 5 WHERE id = 1")
cursor.execute("UPDATE subject SET name = 'Matematika' WHERE id = 1")
cursor.execute("UPDATE school_info SET name = 'Maktab B' WHERE id = 1")

cursor.execute("DELETE FROM student WHERE id = 1")
cursor.execute("DELETE FROM grade WHERE id = 1")
cursor.execute("DELETE FROM subject WHERE id = 1")
cursor.execute("DELETE FROM school_info WHERE id = 1")

conn.commit()

conn.close()