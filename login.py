from flask import Flask, render_template, request, redirect, url_for, flash, session 
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('hw13.db')
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    return render_template('dashboard.html', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        conn=sqlite3.connect('hw13.db')
        conn.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'): 
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form['subject']
        questions_count = int(request.form['num_questions'])
        quiz_date = request.form['quiz_date']

        conn = sqlite3.connect('hw13.db')
        conn.execute('INSERT INTO quizzes (subject, questions_count, quiz_date) VALUES (?, ?,?)',
                     (subject, questions_count, quiz_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')

@app.route('/student/<int:student_id>')
def student_results(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('hw13.db')
    results = conn.execute('''
                           SELECT quizzes.id, quizzes.subject, quizzes.quiz_date, results.score
                           FROM results
                           JOIN quizzes ON results.quiz_id = quizzes.id
                           WHERE results.student_id = ?
                           ''', (student_id)).fetchall()
    conn.close()

    if not results: 
        return f"No Results for student ID {student_id}"
    return render_template('student_results.html', results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('hw13.db')
    students = conn.execute('SELECT id, first_name, last_name FROM students').fetchall()
    quizzes = conn.execute('SELECT id, subject FROM quizzes').fetchall()

    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        quiz_id = int(request.form['quiz_id'])
        score = int(request.form['score'])

        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                     (student_id, quiz_id, score))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_result.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)


