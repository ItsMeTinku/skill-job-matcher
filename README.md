<div align="center">

# 🚀 AI Skill Job Matcher
### Intelligent Career Gap Analysis & Job Recommendation Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge">
  <img src="https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Bootstrap-Frontend-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Deployment-Render-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Live-success?style=for-the-badge">
</p>

<p align="center">
An AI-powered HR-tech platform that analyzes candidate skills, compares them against industry job roles, calculates employability score, detects missing competencies, and recommends personalized upskilling pathways.
</p>

<p align="center">
🌐 <a href="https://skill-job-matcher.onrender.com">Live Demo</a> • ⭐ Star this Repo • 🍴 Fork & Explore
</p>

</div>

---

## 📌 Table of Contents

- Abstract
- Problem Statement
- Proposed Solution
- Core Features
- System Workflow
- Technology Stack
- Project Architecture
- Local Installation Guide
- Cloud Deployment
- Application Screenshots
- Future Scope
- Academic Relevance
- Author
- License
- Support

---

## 📖 Abstract

AI Skill Job Matcher is a smart career intelligence and recruitment assistance platform developed to reduce the gap between candidate skillsets and real-world hiring expectations.

The application enables users to upload their resume or manually enter skills, then performs intelligent comparison against multiple predefined job profiles to determine:

- suitability percentage,
- missing skills,
- learning recommendations,
- employability readiness.

Instead of simply listing jobs, the platform acts as a decision-support engine for students, freshers, and job seekers.

---

## ❗ Problem Statement

Most job seekers do not know:

- which job roles match their current profile,
- which technical skills are missing,
- why they are rejected in screening rounds,
- what they should learn next.

Traditional job portals provide listings but not analytical career guidance.

This project solves that problem using intelligent skill-gap analysis.

---

## 💡 Proposed Solution

The platform performs:

✔ Resume/CV parsing  
✔ Manual skill entry  
✔ Skill-to-job role comparison  
✔ Percentage-based compatibility score  
✔ Missing competency detection  
✔ Personalized skill recommendations  
✔ Career readiness analytics dashboard

---

## 🚀 Core Features

| Feature | Description |
|---------|-------------|
| 🔐 User Authentication | Secure Register/Login/Logout |
| 📄 Resume Upload | PDF / JPG / PNG CV upload |
| 🧠 Skill Matching Engine | Compare candidate skills with job datasets |
| 📊 Match Percentage | Calculate suitability score |
| ✅ Missing Skill Detector | Identify recruiter-required missing skills |
| 💡 Skill Recommendation | Suggest high-value technologies to learn |
| 📈 Improvement Tracking | Visual employability analytics |
| 🔍 Job Filtering | Search multiple career roles |
| ✏️ Editable Skill Dashboard | Update profile dynamically |
| ☁️ Cloud Hosted | Deployable live web application |

---

## 🔄 System Workflow

1. User creates account or logs in  
2. Resume uploaded / skills entered manually  
3. Skills extracted and normalized  
4. Compared against job role database  
5. Match score generated  
6. Missing skills highlighted  
7. Recommended learning path displayed  
8. Career growth graph shown to user

---

## 🛠️ Technology Stack

| Layer | Technologies |
|------|--------------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, Bootstrap |
| Database | SQLite |
| File Processing | Resume Upload Parser |
| Deployment | Render Cloud |
| Version Control | Git & GitHub |

---

## 🧱 Project Architecture

```bash
skill-job-matcher/
│
├── app.py
├── jobs.py
├── database.db
├── requirements.txt
│
├── static/
│   ├── uploads/
│   ├── images/
│   └── css/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── result.html
│   └── profile.html
