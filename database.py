import sqlite3

# Define the courses list
courses_example = [
    {
        "name": "Professional Computing Practice",
        "assignments": {"A1": "2023-04-28", "A2": "2023-05-12", "A3": "2023-05-26"}
    },
    {
        "name": "Further Programming",
        "assignments": {"A2": "2023-05-28"}
    },
    {
        "name": "Foundations of Artificial Intelligence for STEM",
        "assignments": {"A2": "2023-05-12", "A3": "2023-06-02"}
    },
    {
        "name": "Introduction to Cybersecurity",
        "assignments": {"A1": "2023-05-19"}
    }
]

courses = [
    
]

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute (
    '''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

c.execute (
    '''CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        due_date DATE NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
''')

c.execute ('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY
    );
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        user_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY (user_id, course_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
''')

# insert data into tables
def add_courses(courses):
    for course in courses:
        c.execute("INSERT INTO courses (name) VALUES (?)", (course['name'],))
        course_id = c.lastrowid
        for assignment_name, due_date in course['assignments'].items():
            c.execute("INSERT INTO assignments (course_id, name, due_date) VALUES (?, ?, ?)",
                    (course_id, assignment_name, due_date))

# Close the connection
add_courses(courses_example)
conn.commit()
conn.close()
