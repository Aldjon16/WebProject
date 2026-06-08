# 📚 E-Learning Platform (Django)

Një platformë **E-Learning** e ndërtuar me **Django**, e fokusuar në edukimin e fëmijëve.  
Përdoruesit mund të regjistrohen, të kyçen dhe të shikojnë kurset në mënyrë të sigurt.

---

## 🚀 Funksionalitete

- ✅ Regjistrim & Login i përdoruesve
- 🔐 Autentikim me Django Auth
- 📚 Listë kursesh
- 👀 Detaje kursi (vetëm për përdorues të kyçur)
- 🚪 Logout i sigurt
- 🎨 UI me Bootstrap 5
- 🌍 Gjuhë: Shqip 🇦🇱

---

## 🛠 Teknologjitë

- Python 3.12
- Django 5.2
- SQLite
- Bootstrap 5
- HTML / CSS

---

## 📂 Struktura e Projektit

PythonProject1/
│
├── e_learning/ # Project settings
├── edukimi_femijeve/ # Main app
│ ├── templates/
│ ├── views.py
│ ├── urls.py
│ └── models.py
│
├── static/
│ └── images/
│
├── manage.py
├── db.sqlite3
└── README.md


---

## ▶️ Si ta nisësh projektin lokalisht

### 1️⃣ Klono projektin
```bash
git clone https://github.com/USERNAME/e-learning-django.git
cd e-learning-django
2️⃣ Krijo virtual environment
python -m venv .venv
Aktivizo:

Windows:

.venv\Scripts\activate
3️⃣ Instalo varësitë
pip install django
4️⃣ Migro databazën
python manage.py migrate
5️⃣ Krijo superuser (opsionale)
python manage.py createsuperuser
6️⃣ Nise serverin
python manage.py runserver
👉 Hape në browser:
http://127.0.0.1:8000/

🔐 Autentikimi
Kurset shfaqen për të gjithë

Detajet e kursit hapen vetëm pasi të kyçesh

Login / Logout përdorin Django built-in auth

📌 Statusi i Projektit
🟢 Në zhvillim
🔜 Plane:

Regjistrim në kurse

Video lessons

Dashboard për studentë

Deploy online

👤 Autor
Aldjon Kacollja
[README.md](README.md)
Projekt edukativ me Django & Python

📄 Licenca
Ky projekt është për qëllime mësimore.


---

# 📤 SHTO README NË GITHUB

Pas krijimit të README:

```bash
git add README.md
git commit -m "Add professional README"
git push
