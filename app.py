from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from jobs import jobs
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            skills TEXT,
            previous_score REAL,
            current_score REAL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------
@app.route("/")
def home():
    return redirect("/login")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users (name, email, password, skills, previous_score, current_score) VALUES (?, ?, ?, '', 0, 0)",
                (name, email, password)
            )
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        user = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- MATCH LOGIC (UPDATED) ----------
def calculate_match(user_skills):
    results = []
    all_missing_skills = set()

    for job, skills in jobs.items():
        matched_skills = list(set(user_skills) & set(skills))
        missing = list(set(skills) - set(user_skills))

        total = len(skills)
        percentage = (len(matched_skills) / total) * 100 if total > 0 else 0

        all_missing_skills.update(missing)

        results.append({
            "job": job,
            "percentage": round(percentage, 2),
            "matched": matched_skills,
            "missing": missing
        })

    return results, list(all_missing_skills)

# ---------- DASHBOARD ----------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    user = c.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

    # ---------- UPDATE ----------
    if request.method == "POST":

        # CV Upload
        file = request.files.get("cv_file")
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

        # Resume text
        resume_text = request.form.get("resume", "").lower()

        all_skills_db = set([skill for job in jobs.values() for skill in job])
        resume_skills = [skill for skill in all_skills_db if skill in resume_text]

        # EDITABLE SKILL LOGIC (replace old)
        manual_skills = [s.strip().lower() for s in request.form["skills"].split(",") if s.strip()]
        skills = list(set(manual_skills + resume_skills))

        match_data, _ = calculate_match(skills)
        best_score = max([job["percentage"] for job in match_data])

        previous = user[6] if user[6] else 0

        c.execute("""
            UPDATE users 
            SET skills=?, previous_score=?, current_score=? 
            WHERE id=?
        """, (",".join(skills), previous, best_score, session["user_id"]))

        conn.commit()
        return redirect("/dashboard")

    # ---------- DISPLAY ----------
    skills_list = user[4].split(",") if user[4] else []

    match_data, suggestions = calculate_match(skills_list)

    match_data = sorted(match_data, key=lambda x: x["percentage"], reverse=True)
    top_jobs = match_data[:3]

    improvement = (user[6] - user[5]) if user[5] else 0

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        skills=skills_list,
        matches=match_data,
        top_jobs=top_jobs,
        suggestions=suggestions,
        improvement=improvement
    )

if __name__ == "__main__":
    app.run(debug=True)
