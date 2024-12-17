CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
); 

CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    questions_count INTEGER NOT NULL,
    quiz_date TEXT NOT NULL
); 

CREATE TABLE IF NOT EXISTS results (
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
); 
