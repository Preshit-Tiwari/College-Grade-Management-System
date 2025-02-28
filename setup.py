import sqlite3

DATABASE_NAME = "students_marks.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create Students table
    c.execute('''CREATE TABLE IF NOT EXISTS Students (
                    std_id TEXT PRIMARY KEY,
                    std_name TEXT NOT NULL,
                    std_roll_number TEXT NOT NULL,
                    class_id TEXT NOT NULL
                )''')

    # Create Marks table
    c.execute('''CREATE TABLE IF NOT EXISTS Marks (
                    std_id TEXT NOT NULL,
                    subject_id TEXT NOT NULL,
                    marks_obtained INTEGER NOT NULL,
                    class_id TEXT NOT NULL,
                    FOREIGN KEY (std_id) REFERENCES Students (std_id),
                    FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
                )''')

    # Create Subject table
    c.execute('''CREATE TABLE IF NOT EXISTS Subject (
                    subject_id TEXT PRIMARY KEY,
                    subject_name TEXT NOT NULL,
                    max_marks INTEGER NOT NULL,
                    class_id TEXT NOT NULL
                )''')

    # Create Class table
    c.execute('''CREATE TABLE IF NOT EXISTS Class (
                    class_id TEXT PRIMARY KEY,
                    course_id TEXT NOT NULL,
                    semester_id TEXT NOT NULL,
                    branch_id TEXT NOT NULL
                )''')

    # Create Semester table
    c.execute('''CREATE TABLE IF NOT EXISTS Semester (
                    semester_id TEXT PRIMARY KEY,
                    semester_name TEXT NOT NULL
                )''')

    # Create Course table
    c.execute('''CREATE TABLE IF NOT EXISTS Course (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL
                )''')

    # Create Branch table
    c.execute('''CREATE TABLE IF NOT EXISTS Branch (
                    branch_id TEXT PRIMARY KEY,
                    branch_name TEXT NOT NULL
                )''')

    # Create Login table
    c.execute('''CREATE TABLE IF NOT EXISTS Login (
                    login_id TEXT PRIMARY KEY,
                    login_pwd TEXT NOT NULL,
                    login_authority TEXT NOT NULL
                )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")