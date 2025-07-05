# HireHub –  Job Portal 💼

HireHub is a Django-based web application designed as a complete job portal. It connects job seekers with companies by allowing role-based login (Company & Applicant), job posting, resume uploads, and application tracking.

---

## 🚀 Features

* 👤 Role-Based Login System (Company & Applicant)
* 📝 Company Registration, Login, and Job Posting
* 📄 Applicant Registration, Login, and Job Application
* 📂 Resume Upload and Download Feature
* 📬 View & Track Applications (for both companies and applicants)
* 📊 Clean and interactive UI with Bootstrap integration
* 🔐 Password Hashing & Secure Authentication
* 🗓 Dynamic Job Listing with filtering

---

## 💻 Tech Stack

* *Backend:* Django, Python
* *Frontend:* HTML, CSS, Bootstrap, JavaScript
* *Database:* SQLite (default)
* *Others:* Django ORM, File Handling

---

## 🛠 Installation and Setup

Follow these steps to run the project locally:

1. *Clone the repository*

   bash
   git clone https://github.com/yourusername/hirehub.git
   cd hirehub
   

2. *Create and activate virtual environment*

   bash
   python -m venv env
   source env/bin/activate  # for Linux/Mac
   env\Scripts\activate     # for Windows
   

3. *Install the dependencies*

   bash
   pip install -r requirements.txt
   

4. *Apply Migrations*

   bash
   python manage.py makemigrations
   python manage.py migrate
   

5. *Run the development server*

   bash
   python manage.py runserver
   

6. Visit http://127.0.0.1:8000/ in your browser.

---

## 🔐 Default Roles & Access

| Role    | Access                                             |
| ------- | -------------------------------------------------- |
| Company | Register → Login → Post Jobs → View Applicants     |
| Student | Register → Login → Browse Jobs → Apply & Upload CV |

---
