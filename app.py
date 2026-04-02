from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

from jobs import jobs

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        skills TEXT,
        previous_score REAL DEFAULT 0,
        current_score REAL DEFAULT 0,
        file_name TEXT
    )''')

    conn.commit()
    conn.close()

init_db()


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash("Invalid email format!")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters!")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                      (name, email, hashed_password))
            conn.commit()
            conn.close()

            flash("Registration successful!")
            return redirect(url_for('login'))
        except:
            flash("Email already exists!")
            return redirect(url_for('register'))

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!")

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = c.fetchone()

    skills = user[4] or ""
    user_skills = [s.strip().lower() for s in skills.split(",") if s.strip()]

    matched_jobs = []

    for job, req_skills in jobs.items():
        matched = list(set(user_skills).intersection(set(req_skills)))
        total = len(req_skills)
        percentage = (len(matched) / total) * 100 if total > 0 else 0

        if percentage > 0:
            missing = list(set(req_skills) - set(user_skills))

            matched_jobs.append({
                "job": job,
                "percentage": round(percentage, 2),
                "matched": matched,
                "missing": missing
            })

    matched_jobs = sorted(matched_jobs, key=lambda x: x['percentage'], reverse=True)

    # suggestions
    all_missing = []
    for job, req_skills in jobs.items():
        missing = list(set(req_skills) - set(user_skills))
        all_missing.extend(missing)

    suggestions = list(set(all_missing))

    improvement = round((user[6] or 0) - (user[5] or 0), 2)

    conn.close()

    return render_template(
        'dashboard.html',
        user=user,
        skills=user_skills,
        matches=matched_jobs,
        top_jobs=matched_jobs[:3],
        suggestions=suggestions,
        improvement=improvement
    )


# ---------------- UPDATE SKILLS ----------------
@app.route('/update_skills', methods=['POST'])
def update_skills():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    skills = request.form.get('skills', '').strip().lower()
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT current_score FROM users WHERE id=?", (session['user_id'],))
    old_score = c.fetchone()[0] or 0

    new_score = len(skill_list) * 10
    updated_skills = ", ".join(skill_list)

    c.execute("""
        UPDATE users
        SET skills=?, previous_score=?, current_score=?
        WHERE id=?
    """, (updated_skills, old_score, new_score, session['user_id']))

    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))


# ---------------- FILE UPLOAD ----------------
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file = request.files.get('cv_file')

    if file and file.filename != "":
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE users SET file_name=? WHERE id=?",
                  (filename, session['user_id']))
        conn.commit()
        conn.close()

    return redirect(url_for('dashboard'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)