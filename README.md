# 🎯 Skill + Job Matching System (Flask Web App)

## 🌐 Live Demo
👉 [Open Live Website](https://skill-job-matcher.onrender.com)

...
## 📌 Project Overview

This is a web-based application developed using Python Flask that helps users match their skills with different job roles. The system calculates job match percentage, identifies missing skills, and suggests improvements.

---

## 🚀 Features

* 🔐 User Authentication (Register/Login/Logout)
* 🧠 Skill-Based Job Matching
* 📊 Match Percentage Calculation
* ✅ Skills You Have vs Skills Needed
* 💡 Recommended Skills to Learn
* 📈 Improvement Tracking with Graph
* 🔍 Job Search Filter
* ✏️ Editable Skills Section
* 📄 Resume Text Parsing
* 📁 CV Upload (PDF/JPG/PNG)

---

## 🛠️ Tech Stack

* Backend: Python (Flask)
* Frontend: HTML, Bootstrap
* Database: SQLite
* Deployment: Render
* Version Control: GitHub

---

## 📁 Project Structure

```
skill_job_match/
│
├── app.py
├── jobs.py
├── database.db
├── requirements.txt
│
├── static/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/skill-job-matcher.git
cd skill-job-matcher
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Run Application

```
python app.py
```

### 4. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment

This project can be deployed on Render.

### Build Command:

```
pip install -r requirements.txt
```

### Start Command:

```
gunicorn app:app
```

---

## 🎯 Future Improvements

* Use PostgreSQL for scalability
* AI-based resume parsing
* Real-time job API integration
* Advanced analytics dashboard

---

## 🧑‍💻 Author

* BCA Final Year Project
* Developed using Flask

---

## 📌 Note

This project is a prototype and can be scaled for real-world applications.
